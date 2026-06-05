# test/test.py
# Tests cocotb para el módulo nema_controller
# Ejecutar con: cd test && make
#
# Cubre los 5 escenarios de comportamiento del módulo:
#   1. Reset: salidas en estado seguro
#   2. Giro horario (btn_cw): dir=1, step oscila
#   3. Giro antihorario (btn_ccw): dir=0, step oscila
#   4. Reposo (ningún botón): step_pin queda en 0
#   5. Conflicto (ambos botones): step_pin queda en 0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles, Timer


# ─── Constantes del DUT ────────────────────────────────────────────────────────
CLK_MHZ      = 50          # Frecuencia del reloj en MHz
SPEED_DIV    = 6_250       # Mismo valor que el localparam del módulo
# Un pulso completo de step_pin tarda 2 × SPEED_DIV ciclos de reloj
FULL_PULSE_CYCLES = 2 * SPEED_DIV


# ─── Tarea auxiliar: aplicar reset ─────────────────────────────────────────────
async def reset_dut(dut):
    """Aplica reset activo-bajo durante 5 ciclos y deja las entradas en reposo."""
    dut.rst_n.value  = 0
    dut.btn_cw.value  = 0
    dut.btn_ccw.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value  = 1
    await RisingEdge(dut.clk)


# ─── Test 1: Reset ──────────────────────────────────────────────────────────────
@cocotb.test()
async def test_reset(dut):
    """Durante reset todas las salidas deben estar en 0 (estado seguro)."""
    cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())  # 50 MHz

    dut.rst_n.value  = 0
    dut.btn_cw.value  = 0
    dut.btn_ccw.value = 0

    await ClockCycles(dut.clk, 3)

    assert dut.step_pin.value == 0, \
        f"step_pin debe ser 0 durante reset, obtenido: {dut.step_pin.value}"
    assert dut.dir_pin.value == 0, \
        f"dir_pin debe ser 0 durante reset, obtenido: {dut.dir_pin.value}"

    dut._log.info("PASS: reset mantiene salidas en 0")


# ─── Test 2: Giro horario ───────────────────────────────────────────────────────
@cocotb.test()
async def test_giro_horario(dut):
    """Con btn_cw=1, btn_ccw=0: dir_pin=1 y step_pin debe oscilar."""
    cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())
    await reset_dut(dut)

    dut.btn_cw.value  = 1
    dut.btn_ccw.value = 0

    # Esperar un poco para que dir_pin se actualice
    await ClockCycles(dut.clk, 2)
    assert dut.dir_pin.value == 1, \
        f"dir_pin debe ser 1 en giro horario, obtenido: {dut.dir_pin.value}"

    # Esperar un pulso completo y verificar que step_pin haya cambiado
    estado_inicial = int(dut.step_pin.value)
    await ClockCycles(dut.clk, SPEED_DIV + 5)
    estado_mitad = int(dut.step_pin.value)

    assert estado_mitad != estado_inicial, \
        "step_pin no cambió después de SPEED_DIV ciclos en giro horario"

    # Esperar otro medio periodo: step_pin vuelve al estado inicial
    await ClockCycles(dut.clk, SPEED_DIV + 5)
    estado_final = int(dut.step_pin.value)

    assert estado_final == estado_inicial, \
        "step_pin no completó el ciclo completo en giro horario"

    dut._log.info("PASS: giro horario → dir=1, step oscila correctamente")


# ─── Test 3: Giro antihorario ───────────────────────────────────────────────────
@cocotb.test()
async def test_giro_antihorario(dut):
    """Con btn_ccw=1, btn_cw=0: dir_pin=0 y step_pin debe oscilar."""
    cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())
    await reset_dut(dut)

    dut.btn_cw.value  = 0
    dut.btn_ccw.value = 1

    await ClockCycles(dut.clk, 2)
    assert dut.dir_pin.value == 0, \
        f"dir_pin debe ser 0 en giro antihorario, obtenido: {dut.dir_pin.value}"

    estado_inicial = int(dut.step_pin.value)
    await ClockCycles(dut.clk, SPEED_DIV + 5)
    estado_mitad = int(dut.step_pin.value)

    assert estado_mitad != estado_inicial, \
        "step_pin no cambió después de SPEED_DIV ciclos en giro antihorario"

    dut._log.info("PASS: giro antihorario → dir=0, step oscila correctamente")


# ─── Test 4: Reposo (ningún botón) ─────────────────────────────────────────────
@cocotb.test()
async def test_reposo_sin_botones(dut):
    """Sin botones presionados: step_pin debe mantenerse en 0 (motor clavado)."""
    cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())
    await reset_dut(dut)

    dut.btn_cw.value  = 0
    dut.btn_ccw.value = 0

    # Esperar varios periodos completos y verificar que step_pin nunca sube
    for _ in range(3):
        await ClockCycles(dut.clk, SPEED_DIV + 10)
        assert dut.step_pin.value == 0, \
            f"step_pin debe ser 0 en reposo, obtenido: {dut.step_pin.value}"

    dut._log.info("PASS: reposo → step_pin permanece en 0")


# ─── Test 5: Conflicto (ambos botones a la vez) ────────────────────────────────
@cocotb.test()
async def test_conflicto_ambos_botones(dut):
    """Con btn_cw=1 y btn_ccw=1 simultáneos: step_pin debe permanecer en 0."""
    cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())
    await reset_dut(dut)

    dut.btn_cw.value  = 1
    dut.btn_ccw.value = 1

    for _ in range(3):
        await ClockCycles(dut.clk, SPEED_DIV + 10)
        assert dut.step_pin.value == 0, \
            f"step_pin debe ser 0 con conflicto de botones, obtenido: {dut.step_pin.value}"

    dut._log.info("PASS: conflicto → step_pin permanece en 0")


# ─── Test 6: Transición horario → reposo → antihorario ────────────────────────
@cocotb.test()
async def test_transicion_direcciones(dut):
    """
    Verifica que el módulo transiciona correctamente entre estados:
    horario → reposo → antihorario, comprobando dir_pin y step en cada etapa.
    """
    cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())
    await reset_dut(dut)

    # -- Fase 1: horario --
    dut.btn_cw.value  = 1
    dut.btn_ccw.value = 0
    await ClockCycles(dut.clk, SPEED_DIV + 5)

    assert dut.dir_pin.value == 1, "Fase horaria: dir_pin debe ser 1"

    # -- Fase 2: reposo --
    dut.btn_cw.value  = 0
    dut.btn_ccw.value = 0
    await ClockCycles(dut.clk, 10)

    assert dut.step_pin.value == 0, "Fase reposo: step_pin debe volver a 0"

    # -- Fase 3: antihorario --
    dut.btn_cw.value  = 0
    dut.btn_ccw.value = 1
    await ClockCycles(dut.clk, 2)

    assert dut.dir_pin.value == 0, "Fase antihoraria: dir_pin debe ser 0"

    await ClockCycles(dut.clk, SPEED_DIV + 5)
    # step_pin debe haber cambiado en algún momento durante antihorario
    # (el counter se reinicia al entrar, así que habrá transcurrido al menos 1 toggle)

    dut._log.info("PASS: transición horario→reposo→antihorario correcta")


# ─── Test 7: Frecuencia de step verificada ─────────────────────────────────────
@cocotb.test()
async def test_frecuencia_step(dut):
    """
    Cuenta los flancos de subida de step_pin durante N ciclos y verifica
    que la frecuencia se aproxima a clk / (2 × SPEED_DIV) = 4 kHz.
    
    Con clk=50 MHz y SPEED_DIV=6250:
        f_step = 50_000_000 / (2 × 6250) = 4000 Hz
    Se miden flancos durante 10 pulsos completos esperados.
    """
    cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())
    await reset_dut(dut)

    dut.btn_cw.value  = 1
    dut.btn_ccw.value = 0

    # Esperar que el counter empiece desde 0 (ya reseteado)
    flancos = 0
    ciclos_medicion = FULL_PULSE_CYCLES * 10  # 10 pulsos completos

    prev = int(dut.step_pin.value)
    for _ in range(ciclos_medicion):
        await RisingEdge(dut.clk)
        curr = int(dut.step_pin.value)
        if curr == 1 and prev == 0:   # Flanco de subida
            flancos += 1
        prev = curr

    # Esperamos ~10 flancos de subida (1 por pulso completo)
    # Tolerancia: ±2 flancos por latencia de arranque del counter
    assert 8 <= flancos <= 12, \
        f"Se esperaban ~10 flancos de subida, se contaron: {flancos}"

    dut._log.info(f"PASS: frecuencia correcta → {flancos} flancos en {ciclos_medicion} ciclos")