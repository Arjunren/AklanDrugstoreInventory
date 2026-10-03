namespace AklanDrugstoreInventory.Models;

public class AuditEntry
{
    public DateTime Time { get; set; }
    public string Action { get; set; } = string.Empty;
    public string Details { get; set; } = string.Empty;
}
