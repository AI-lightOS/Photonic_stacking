//============================================================================
// TFLN_AI_NODE_X2 - Top-Level Board Verilog Model
// Board-level interconnect and I/O definition for simulation/verification
//============================================================================
`timescale 1ns / 1ps

module tfln_ai_node_x2_top (
    // =========================================================
    // Power Rails
    // =========================================================
    input  wire        VIN_12V,          // 12V main input
    input  wire        VIN_12V_RTN,      // 12V return
    output wire        V_CORE,           // 0.8V core (from VRM)
    output wire        V_IO,             // 1.1V I/O
    output wire        V_DDQ,            // 1.1V DDR5
    output wire        V_3V3,            // 3.3V auxiliary

    // =========================================================
    // PCIe Gen6 x16 Interfaces (8 slots)
    // =========================================================
    input  wire [7:0]  PCIE_REFCLK_P,
    input  wire [7:0]  PCIE_REFCLK_N,
    inout  wire [127:0] PCIE_TX_P,       // 16 lanes x 8 slots
    inout  wire [127:0] PCIE_TX_N,
    inout  wire [127:0] PCIE_RX_P,
    inout  wire [127:0] PCIE_RX_N,
    input  wire [7:0]  PCIE_PERST_N,
    output wire [7:0]  PCIE_WAKE_N,

    // =========================================================
    // DDR5 Interfaces (4 DIMMs)
    // =========================================================
    output wire [3:0]  DDR5_CK_P,
    output wire [3:0]  DDR5_CK_N,
    output wire [3:0]  DDR5_RESET_N,
    output wire [3:0]  DDR5_CS_N,
    output wire [55:0] DDR5_CA,          // 14 command/address per DIMM
    inout  wire [255:0] DDR5_DQ,         // 64 data bits per DIMM
    inout  wire [31:0] DDR5_DQS_P,      // 8 strobes per DIMM
    inout  wire [31:0] DDR5_DQS_N,

    // =========================================================
    // TFLN Photonic Interfaces
    // =========================================================
    output wire [15:0] TFLN_RF_P,        // RF modulator drive (+)
    output wire [15:0] TFLN_RF_N,        // RF modulator drive (-)
    output wire [7:0]  TFLN_BIAS,        // DC bias for modulators
    input  wire [7:0]  TFLN_MON,         // Monitor photodiode inputs

    // =========================================================
    // NVMe M.2 Interfaces (4 slots)
    // =========================================================
    input  wire [3:0]  NVME_REFCLK_P,
    input  wire [3:0]  NVME_REFCLK_N,
    inout  wire [15:0] NVME_TX_P,        // 4 lanes x 4 slots
    inout  wire [15:0] NVME_TX_N,
    inout  wire [15:0] NVME_RX_P,
    inout  wire [15:0] NVME_RX_N,

    // =========================================================
    // SerDes Inter-Die Links (AI Unit 1 <-> AI Unit 2)
    // =========================================================
    inout  wire [15:0] SERDES_U1_U2_P,
    inout  wire [15:0] SERDES_U1_U2_N,

    // =========================================================
    // System Management
    // =========================================================
    input  wire        SYS_CLK_100M,
    input  wire        SYS_RESET_N,
    output wire        PGOOD,
    output wire [3:0]  STATUS_LED
);

    // =========================================================
    // Internal Wires
    // =========================================================
    wire        vcore_pgood;
    wire        vio_pgood;
    wire        vddq_pgood;
    wire        v3v3_pgood;

    // VRM phase currents (24 phases each)
    wire [23:0] vrm_u5_phase_pwm;
    wire [23:0] vrm_u6_phase_pwm;
    wire [23:0] vrm_u7_phase_pwm;
    wire [23:0] vrm_u8_phase_pwm;

    // =========================================================
    // U1: AI Compute Unit 1 (BGA256)
    // =========================================================
    ai_compute_unit u1_ai (
        .V_CORE         (V_CORE),
        .V_IO           (V_IO),
        .GND            (1'b0),
        .PCIE_TX_P      (PCIE_TX_P[63:0]),
        .PCIE_TX_N      (PCIE_TX_N[63:0]),
        .PCIE_RX_P      (PCIE_RX_P[63:0]),
        .PCIE_RX_N      (PCIE_RX_N[63:0]),
        .DDR5_DQ        (DDR5_DQ[127:0]),
        .DDR5_DQS_P     (DDR5_DQS_P[15:0]),
        .DDR5_DQS_N     (DDR5_DQS_N[15:0]),
        .DDR5_CA        (DDR5_CA[27:0]),
        .DDR5_CK_P      (DDR5_CK_P[1:0]),
        .DDR5_CK_N      (DDR5_CK_N[1:0]),
        .SERDES_TX_P    (SERDES_U1_U2_P),
        .SERDES_TX_N    (SERDES_U1_U2_N),
        .TFLN_RF_P      (TFLN_RF_P[7:0]),
        .TFLN_RF_N      (TFLN_RF_N[7:0]),
        .NVME_TX_P      (NVME_TX_P[7:0]),
        .NVME_TX_N      (NVME_TX_N[7:0]),
        .NVME_RX_P      (NVME_RX_P[7:0]),
        .NVME_RX_N      (NVME_RX_N[7:0]),
        .SYS_CLK        (SYS_CLK_100M),
        .SYS_RESET_N    (SYS_RESET_N)
    );

    // =========================================================
    // U2: AI Compute Unit 2 (BGA256)
    // =========================================================
    ai_compute_unit u2_ai (
        .V_CORE         (V_CORE),
        .V_IO           (V_IO),
        .GND            (1'b0),
        .PCIE_TX_P      (PCIE_TX_P[127:64]),
        .PCIE_TX_N      (PCIE_TX_N[127:64]),
        .PCIE_RX_P      (PCIE_RX_P[127:64]),
        .PCIE_RX_N      (PCIE_RX_N[127:64]),
        .DDR5_DQ        (DDR5_DQ[255:128]),
        .DDR5_DQS_P     (DDR5_DQS_P[31:16]),
        .DDR5_DQS_N     (DDR5_DQS_N[31:16]),
        .DDR5_CA        (DDR5_CA[55:28]),
        .DDR5_CK_P      (DDR5_CK_P[3:2]),
        .DDR5_CK_N      (DDR5_CK_N[3:2]),
        .SERDES_TX_P    (SERDES_U1_U2_P),
        .SERDES_TX_N    (SERDES_U1_U2_N),
        .TFLN_RF_P      (TFLN_RF_P[15:8]),
        .TFLN_RF_N      (TFLN_RF_N[15:8]),
        .NVME_TX_P      (NVME_TX_P[15:8]),
        .NVME_TX_N      (NVME_TX_N[15:8]),
        .NVME_RX_P      (NVME_RX_P[15:8]),
        .NVME_RX_N      (NVME_RX_N[15:8]),
        .SYS_CLK        (SYS_CLK_100M),
        .SYS_RESET_N    (SYS_RESET_N)
    );

    // =========================================================
    // U3: TFLN Photonic Engine 1
    // =========================================================
    tfln_photonic_engine u3_tfln (
        .RF_IN_P        (TFLN_RF_P[7:0]),
        .RF_IN_N        (TFLN_RF_N[7:0]),
        .BIAS           (TFLN_BIAS[3:0]),
        .MON_PD         (TFLN_MON[3:0]),
        .V_IO           (V_IO),
        .GND            (1'b0)
    );

    // =========================================================
    // U4: TFLN Photonic Engine 2
    // =========================================================
    tfln_photonic_engine u4_tfln (
        .RF_IN_P        (TFLN_RF_P[15:8]),
        .RF_IN_N        (TFLN_RF_N[15:8]),
        .BIAS           (TFLN_BIAS[7:4]),
        .MON_PD         (TFLN_MON[7:4]),
        .V_IO           (V_IO),
        .GND            (1'b0)
    );

    // =========================================================
    // VRM Subsystem (U5-U8: 24-phase DrMOS each)
    // =========================================================
    vrm_drmos_24phase u5_vrm (
        .VIN            (VIN_12V),
        .VOUT           (V_CORE),
        .PGOOD          (vcore_pgood),
        .PHASE_PWM      (vrm_u5_phase_pwm),
        .GND            (1'b0)
    );

    vrm_drmos_24phase u6_vrm (
        .VIN            (VIN_12V),
        .VOUT           (V_IO),
        .PGOOD          (vio_pgood),
        .PHASE_PWM      (vrm_u6_phase_pwm),
        .GND            (1'b0)
    );

    vrm_drmos_24phase u7_vrm (
        .VIN            (VIN_12V),
        .VOUT           (V_DDQ),
        .PGOOD          (vddq_pgood),
        .PHASE_PWM      (vrm_u7_phase_pwm),
        .GND            (1'b0)
    );

    vrm_drmos_24phase u8_vrm (
        .VIN            (VIN_12V),
        .VOUT           (V_3V3),
        .PGOOD          (v3v3_pgood),
        .PHASE_PWM      (vrm_u8_phase_pwm),
        .GND            (1'b0)
    );

    // =========================================================
    // Power Good Aggregation
    // =========================================================
    assign PGOOD = vcore_pgood & vio_pgood & vddq_pgood & v3v3_pgood;
    assign STATUS_LED = {v3v3_pgood, vddq_pgood, vio_pgood, vcore_pgood};

endmodule
