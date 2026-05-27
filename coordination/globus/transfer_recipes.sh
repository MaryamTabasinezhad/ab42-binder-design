#!/bin/bash
# Globus transfer recipes for the ab42-binder-design project.
# Source your cluster env file first, then run the relevant function.
#
# Usage:
#   source clusters/<cluster>.env
#   source coordination/globus/transfer_recipes.sh
#   transfer_accepted_to_frontenac

# Endpoint IDs
EP_FRONTENAC="79136050-41db-11f1-8063-0afffe4617ab"
EP_NIBI="07baf15f-d7fd-4b6a-bf8a-5b5ef2e229d3"
EP_NARVAL="a1713da6-098f-40e6-b3aa-034efe8b6e5b"

# Base paths per cluster
BP_FRONTENAC="/global/project/hpcg6049/protein"
BP_NIBI="/home/ghaedi/projects/def-ghaedi/ghaedi/protein"
BP_NARVAL="/home/ghaedi/projects/def-ghaedi/ghaedi/protein"

transfer_accepted_to_frontenac() {
    local src_ep="${GLOBUS_ENDPOINT}"
    local src_base="${GLOBUS_BASE_PATH}"
    local label="${CLUSTER_NAME}_accepted_$(date +%Y%m%d)"

    echo "Transferring accepted PDBs from ${CLUSTER_NAME} to Frontenac..."
    globus transfer \
        "${src_ep}:${src_base}/alzheimer/bindcraft/designs/Accepted/" \
        "${EP_FRONTENAC}:${BP_FRONTENAC}/alzheimer/bindcraft/sync/from_${CLUSTER_NAME}/designs_accepted/" \
        --recursive --sync-level checksum --label "${label}"

    echo "Transferring final_design_stats.csv..."
    globus transfer \
        "${src_ep}:${src_base}/alzheimer/bindcraft/designs/final_design_stats.csv" \
        "${EP_FRONTENAC}:${BP_FRONTENAC}/alzheimer/bindcraft/sync/from_${CLUSTER_NAME}/final_design_stats_${CLUSTER_NAME}.csv" \
        --label "${label}_stats"
}

transfer_parallel_accepted_to_frontenac() {
    local src_ep="${GLOBUS_ENDPOINT}"
    local src_base="${GLOBUS_BASE_PATH}"

    for i in 1 2 3 4; do
        local dir="${src_base}/alzheimer/bindcraft/designs_p${i}/Accepted/"
        echo "Transferring parallel job p${i} accepted PDBs..."
        globus transfer \
            "${src_ep}:${dir}" \
            "${EP_FRONTENAC}:${BP_FRONTENAC}/alzheimer/bindcraft/sync/from_${CLUSTER_NAME}/designs_p${i}_accepted/" \
            --recursive --sync-level checksum \
            --label "${CLUSTER_NAME}_p${i}_accepted_$(date +%Y%m%d)" 2>/dev/null || echo "  (p${i} not found, skipping)"
    done
}

transfer_counter_screen_results_to_frontenac() {
    local src_ep="${GLOBUS_ENDPOINT}"
    local src_base="${GLOBUS_BASE_PATH}"

    echo "Transferring Stage 3 counter-screen results..."
    globus transfer \
        "${src_ep}:${src_base}/alzheimer/bindcraft/filtering/" \
        "${EP_FRONTENAC}:${BP_FRONTENAC}/alzheimer/bindcraft/sync/from_${CLUSTER_NAME}/filtering/" \
        --recursive --sync-level checksum \
        --label "${CLUSTER_NAME}_stage3_$(date +%Y%m%d)"
}
