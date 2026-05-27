# Globus Endpoints

## Endpoint Registry

| Cluster | Endpoint ID | Type | Base Path |
|---------|------------|------|-----------|
| Frontenac | `79136050-41db-11f1-8063-0afffe4617ab` | Personal | `/global/project/hpcg6049/protein` |
| Nibi | `07baf15f-d7fd-4b6a-bf8a-5b5ef2e229d3` | Institutional | `/home/ghaedi/projects/def-ghaedi/ghaedi/protein` |
| Narval | `a1713da6-098f-40e6-b3aa-034efe8b6e5b` | Institutional | `/home/ghaedi/projects/def-ghaedi/ghaedi/protein` |

## Connectivity

- **Institutional to institutional:** Direct (Nibi <-> Narval works)
- **Institutional to Frontenac:** Direct (Nibi/Narval -> Frontenac works)
- **Frontenac to institutional:** Direct (Frontenac -> Nibi/Narval works)
- **Personal to personal:** Requires institutional relay (not applicable here unless Limestone VM is involved)

## Frontenac GCP

Frontenac's Globus Connect Personal runs on the **transfer node** `frntxfr.frontenac.local`, not the login node. To start GCP:

```bash
ssh transfer.cac.queensu.ca
~/globusconnectpersonal-3.2.8/globusconnectpersonal -start &
```

GCP must be running for any transfer involving Frontenac.

## Globus CLI

| Cluster | How to get `globus` command |
|---------|---------------------------|
| Frontenac | `conda activate rnaseq && globus ...` |
| Nibi | `pip install --user globus-cli` (or module if available) |
| Narval | `pip install --user globus-cli` (or module if available) |

## Transfer recipes

See `transfer_recipes.sh` in this directory for reusable commands.
