//============================================================================
// VRM DrMOS 24-Phase Buck Converter Model
// Multi-phase voltage regulator for high-current delivery (1000A+)
//============================================================================
`timescale 1ns / 1ps

module vrm_drmos_24phase (
    // Power
    input  wire        VIN,         // 12V input
    output reg         VOUT,        // Regulated output
    output wire        PGOOD,       // Power good indicator

    // Phase control
    output wire [23:0] PHASE_PWM,   // Individual phase PWM outputs

    input  wire        GND
);

    // =========================================================
    // VRM Parameters
    // =========================================================
    parameter real VIN_NOM      = 12.0;     // Nominal input voltage
    parameter real VOUT_TARGET  = 0.8;      // Target output voltage
    parameter real IOUT_MAX     = 1200.0;   // Max output current (A)
    parameter real EFFICIENCY   = 0.92;     // Typical efficiency
    parameter real FSW_KHZ      = 600.0;    // Switching frequency
    parameter integer NUM_PHASES = 24;      // Number of phases
    parameter real IPHASE_MAX   = 50.0;     // Max current per phase (A)
    parameter real RIPPLE_MV    = 5.0;      // Output ripple (mV p-p)

    // =========================================================
    // Phase Generator (360/24 = 15 degree spacing)
    // =========================================================
    reg [23:0] phase_state;
    reg [4:0]  phase_counter;
    reg        pwm_clk;
    reg        startup_done;
    integer    i;

    initial begin
        phase_state  = 24'h000001;
        phase_counter = 0;
        pwm_clk      = 0;
        startup_done = 0;
        VOUT         = 0;
    end

    // Switching clock (~600 kHz)
    always #833 pwm_clk = ~pwm_clk;

    // Phase rotation
    always @(posedge pwm_clk) begin
        if (VIN) begin
            phase_counter <= phase_counter + 1;
            if (phase_counter >= NUM_PHASES - 1)
                phase_counter <= 0;
            phase_state <= {phase_state[22:0], phase_state[23]};

            // Soft-start ramp
            if (!startup_done) begin
                #100;  // 100ns startup delay per step
                startup_done <= 1;
            end
            VOUT <= VIN & startup_done;
        end else begin
            phase_state  <= 24'h000001;
            phase_counter <= 0;
            startup_done <= 0;
            VOUT         <= 0;
        end
    end

    assign PHASE_PWM = phase_state;
    assign PGOOD = startup_done & VIN;

    // =========================================================
    // Thermal Model (simplified)
    // =========================================================
    // Power dissipation per phase:
    //   P_loss = IOUT_MAX / NUM_PHASES * VOUT * (1 - EFFICIENCY) / EFFICIENCY
    //   = 1200/24 * 0.8 * 0.087 = ~3.5W per phase
    //   Total: ~84W dissipated across VRM array
    //   Thermal relief: SOLID (no spokes) for maximum heat transfer

endmodule
