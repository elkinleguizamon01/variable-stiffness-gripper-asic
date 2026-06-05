# test/Makefile
# Uso: cd test && make
# Requiere: iverilog, cocotb, pytest  (pip install cocotb pytest)

SIM         ?= icarus
TOPLEVEL_LANG ?= verilog

# Agrega aquí todos tus archivos fuente (rutas relativas a esta carpeta)
VERILOG_SOURCES  = $(PWD)/../src/nema_controller.v

# Nombre exacto del módulo top del testbench (tb.v)
TOPLEVEL = tb

# Módulo Python de tests (sin extensión .py)
MODULE = test

include $(shell cocotb-config --makefiles)/Makefile.sim
