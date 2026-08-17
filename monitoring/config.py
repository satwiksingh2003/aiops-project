# =====================================================
# AIOps Configuration
# =====================================================

# Model
MODEL_PATH = "monitoring/isolation_forest_model.pkl"

# Monitoring
CHECK_INTERVAL = 10      # seconds

# Feature Columns
FEATURES = [
    "CPU",
    "Memory_MB",
    "Network_RX_KBps",
    "Network_TX_KBps"
]

# Thresholds
CPU_THRESHOLD = 0.10
MEMORY_THRESHOLD = 400
NETWORK_THRESHOLD = 0.25

# Logging
LOG_FILE = "logs/aiops.log"

# Remediation
EXECUTE_REMEDIATION = False

# Kubernetes
NAMESPACE = "robot-shop"