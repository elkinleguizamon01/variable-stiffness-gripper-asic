module nema_controller (
    input  wire clk,          // Reloj principal de la FPGA (50 MHz)
    input  wire rst_n,        // Reset activo bajo
    
    // Entradas de control (Deben venir del módulo debouncer)
    input  wire btn_cw,       // Botón para giro Horario (Derecha)
    input  wire btn_ccw,      // Botón para giro Antihorario (Izquierda)
    
    // Salidas físicas hacia el Driver (A4988 / DRV8825)
    output wire step_pin,     // Tren de pulsos
    output reg  dir_pin       // Dirección de giro
);

    // ==========================================
    // CONFIGURACIÓN DE VELOCIDAD
    // ==========================================
    // Con un reloj de 50 MHz, contar hasta 25,000 genera una inversión 
    // de la señal cada 0.5 milisegundos.
    // Esto crea un pulso completo (1 y 0) cada 1 ms -> Frecuencia = 1 kHz.
    localparam SPEED_DIV = 16'd6_250; 

    reg [15:0] step_counter;
    reg        step_reg;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            step_counter <= 16'd0;
            step_reg     <= 1'b0;
            dir_pin      <= 1'b0;
        end else begin
            // 1. Giro en un sentido (Horario)
            if (btn_cw && !btn_ccw) begin
                dir_pin <= 1'b1;
                
                if (step_counter >= SPEED_DIV) begin
                    step_counter <= 16'd0;
                    step_reg     <= ~step_reg; // Invierte el estado del pin STEP
                end else begin
                    step_counter <= step_counter + 1'b1;
                end
            end
            // 2. Giro en sentido opuesto (Antihorario)
            else if (btn_ccw && !btn_cw) begin
                dir_pin <= 1'b0;
                
                if (step_counter >= SPEED_DIV) begin
                    step_counter <= 16'd0;
                    step_reg     <= ~step_reg;
                end else begin
                    step_counter <= step_counter + 1'b1;
                end
            end
            // 3. Reposo (Ningún botón o ambos presionados a la vez)
            else begin
                step_counter <= 16'd0;
                step_reg     <= 1'b0; // Mantiene la señal en bajo, el motor se clava en su posición
            end
        end
    end

    // Asignación continua al puerto de salida
    assign step_pin = step_reg;

endmodule