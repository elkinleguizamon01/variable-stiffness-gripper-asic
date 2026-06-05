// Testbench para nema_controller
// Compatible con cocotb + iverilog
// Colócalo en: test/tb.v
 
`timescale 1ns / 1ps
 
module nema_controller_tb ();
 
    // --------------------------------------------------------
    // Señales que conectan con el DUT (Device Under Test)
    // --------------------------------------------------------
    reg  clk;
    reg  rst_n;
    reg  btn_cw;
    reg  btn_ccw;
 
    wire step_pin;
    wire dir_pin;
 
    // --------------------------------------------------------
    // Instancia del módulo bajo prueba
    // Cambia "nema_controller" si renombraste el módulo
    // --------------------------------------------------------
    nema_controller dut (
        .clk     (clk),
        .rst_n   (rst_n),
        .btn_cw  (btn_cw),
        .btn_ccw (btn_ccw),
        .step_pin(step_pin),
        .dir_pin (dir_pin)
    );
 
    // --------------------------------------------------------
    // Generación de reloj: 50 MHz → periodo = 20 ns
    // --------------------------------------------------------
    initial clk = 1'b0;
    always #10 clk = ~clk;   // Toggle cada 10 ns → 20 ns de periodo
 
    // --------------------------------------------------------
    // Volcado de formas de onda (abrir con GTKWave: gtkwave tb.vcd)
    // --------------------------------------------------------
    initial begin
        $dumpfile("tb.vcd");
        $dumpvars(0, tb);
    end
 
endmodule