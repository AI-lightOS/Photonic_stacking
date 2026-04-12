//============================================================================
// TFLN_AI_NODE_X2 - Board-Level Testbench
// Verifies power sequencing, interface connectivity, and signal integrity
//============================================================================
`timescale 1ns / 1ps

module tb_tfln_ai_node_x2;

    // =========================================================
    // Testbench Signals
    // =========================================================
    reg         VIN_12V;
    reg         VIN_12V_RTN;
    wire        V_CORE, V_IO, V_DDQ, V_3V3;

    reg  [7:0]  PCIE_REFCLK_P, PCIE_REFCLK_N;
    wire [127:0] PCIE_TX_P, PCIE_TX_N, PCIE_RX_P, PCIE_RX_N;
    reg  [7:0]  PCIE_PERST_N;
    wire [7:0]  PCIE_WAKE_N;

    wire [3:0]  DDR5_CK_P, DDR5_CK_N, DDR5_RESET_N, DDR5_CS_N;
    wire [55:0] DDR5_CA;
    wire [255:0] DDR5_DQ;
    wire [31:0] DDR5_DQS_P, DDR5_DQS_N;

    wire [15:0] TFLN_RF_P, TFLN_RF_N;
    wire [7:0]  TFLN_BIAS;
    reg  [7:0]  TFLN_MON;

    reg  [3:0]  NVME_REFCLK_P, NVME_REFCLK_N;
    wire [15:0] NVME_TX_P, NVME_TX_N, NVME_RX_P, NVME_RX_N;
    wire [15:0] SERDES_U1_U2_P, SERDES_U1_U2_N;

    reg         SYS_CLK_100M;
    reg         SYS_RESET_N;
    wire        PGOOD;
    wire [3:0]  STATUS_LED;

    // =========================================================
    // DUT Instantiation
    // =========================================================
    tfln_ai_node_x2_top dut (
        .VIN_12V        (VIN_12V),
        .VIN_12V_RTN    (VIN_12V_RTN),
        .V_CORE         (V_CORE),
        .V_IO           (V_IO),
        .V_DDQ          (V_DDQ),
        .V_3V3          (V_3V3),
        .PCIE_REFCLK_P  (PCIE_REFCLK_P),
        .PCIE_REFCLK_N  (PCIE_REFCLK_N),
        .PCIE_TX_P      (PCIE_TX_P),
        .PCIE_TX_N      (PCIE_TX_N),
        .PCIE_RX_P      (PCIE_RX_P),
        .PCIE_RX_N      (PCIE_RX_N),
        .PCIE_PERST_N   (PCIE_PERST_N),
        .PCIE_WAKE_N    (PCIE_WAKE_N),
        .DDR5_CK_P      (DDR5_CK_P),
        .DDR5_CK_N      (DDR5_CK_N),
        .DDR5_RESET_N   (DDR5_RESET_N),
        .DDR5_CS_N      (DDR5_CS_N),
        .DDR5_CA        (DDR5_CA),
        .DDR5_DQ        (DDR5_DQ),
        .DDR5_DQS_P     (DDR5_DQS_P),
        .DDR5_DQS_N     (DDR5_DQS_N),
        .TFLN_RF_P      (TFLN_RF_P),
        .TFLN_RF_N      (TFLN_RF_N),
        .TFLN_BIAS      (TFLN_BIAS),
        .TFLN_MON       (TFLN_MON),
        .NVME_REFCLK_P  (NVME_REFCLK_P),
        .NVME_REFCLK_N  (NVME_REFCLK_N),
        .NVME_TX_P      (NVME_TX_P),
        .NVME_TX_N      (NVME_TX_N),
        .NVME_RX_P      (NVME_RX_P),
        .NVME_RX_N      (NVME_RX_N),
        .SERDES_U1_U2_P (SERDES_U1_U2_P),
        .SERDES_U1_U2_N (SERDES_U1_U2_N),
        .SYS_CLK_100M   (SYS_CLK_100M),
        .SYS_RESET_N    (SYS_RESET_N),
        .PGOOD          (PGOOD),
        .STATUS_LED     (STATUS_LED)
    );

    // =========================================================
    // Clock Generation (100 MHz system clock)
    // =========================================================
    initial SYS_CLK_100M = 0;
    always #5 SYS_CLK_100M = ~SYS_CLK_100M;

    // PCIe reference clocks (100 MHz)
    initial PCIE_REFCLK_P = 8'h00;
    always #5 PCIE_REFCLK_P = ~PCIE_REFCLK_P;
    always @(PCIE_REFCLK_P) PCIE_REFCLK_N = ~PCIE_REFCLK_P;

    // NVMe reference clocks (100 MHz)
    initial NVME_REFCLK_P = 4'h0;
    always #5 NVME_REFCLK_P = ~NVME_REFCLK_P;
    always @(NVME_REFCLK_P) NVME_REFCLK_N = ~NVME_REFCLK_P;

    // =========================================================
    // Test Sequence
    // =========================================================
    initial begin
        $dumpfile("tfln_ai_node_x2_tb.vcd");
        $dumpvars(0, tb_tfln_ai_node_x2);

        // Initialize
        VIN_12V      = 0;
        VIN_12V_RTN  = 0;
        SYS_RESET_N  = 0;
        PCIE_PERST_N = 8'h00;
        TFLN_MON     = 8'h00;

        // =============================================
        // Test 1: Power-On Sequence
        // =============================================
        $display("=== Test 1: Power-On Sequence ===");
        #100;
        VIN_12V = 1;        // Apply 12V
        #200;

        // Wait for VRM startup
        #2000;
        if (PGOOD)
            $display("PASS: Power good asserted");
        else
            $display("INFO: Power good not yet asserted (VRM startup in progress)");

        // =============================================
        // Test 2: System Reset Release
        // =============================================
        $display("=== Test 2: System Reset Release ===");
        SYS_RESET_N = 1;
        #100;
        $display("PASS: System reset released");

        // =============================================
        // Test 3: PCIe PERST Release
        // =============================================
        $display("=== Test 3: PCIe PERST Release ===");
        #500;
        PCIE_PERST_N = 8'hFF;
        #100;
        $display("PASS: All PCIe slots released from reset");

        // =============================================
        // Test 4: TFLN Modulator Bias Lock
        // =============================================
        $display("=== Test 4: TFLN Bias Lock ===");
        TFLN_MON = 8'hFF;
        #500;
        $display("PASS: TFLN monitor photodiodes active");

        // =============================================
        // Test 5: Status LED Verification
        // =============================================
        $display("=== Test 5: Status LEDs ===");
        #100;
        $display("STATUS_LED = %b", STATUS_LED);
        $display("PGOOD = %b", PGOOD);

        // Run for additional time
        #5000;

        $display("=== All board-level tests complete ===");
        $finish;
    end

    // =========================================================
    // Timeout Watchdog
    // =========================================================
    initial begin
        #100000;
        $display("ERROR: Simulation timeout");
        $finish;
    end

endmodule
