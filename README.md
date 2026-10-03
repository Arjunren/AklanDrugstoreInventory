# Aklan Drugstore Inventory

A simple student project made with .NET MAUI for a local drugstore in Aklan, Panay Island. The application runs on Windows and Android and replaces basic manual inventory checking with an easy local system.

## Features

- Local login and logout
- Menu navigation
- Add, update, delete, and display products
- Dashboard totals and a stock-level bar chart
- Low-stock count for products with 10 units or fewer
- Audit trail for login and inventory transactions
- Local JSON storage using the device application-data folder

## Demo login

- Username: `admin`
- Password: `admin123`

This fixed login is intended only for a classroom demonstration. A production application should store password hashes securely and use proper authentication.

## Requirements

- Visual Studio 2026 with the .NET MAUI workload
- .NET 10 SDK
- Windows 10/11 or an Android emulator/device

## Open and run in Visual Studio

1. Open `AklanDrugstoreInventory.sln` in Visual Studio. This traditional solution format is the safest option.
2. Select `Windows Machine` or an Android emulator in the debug target list.
3. Press `F5`.
4. Log in with the demo account.

## Command-line build

```powershell
dotnet build AklanDrugstoreInventory.csproj -f net10.0-windows10.0.19041.0
dotnet build AklanDrugstoreInventory.csproj -f net10.0-android
```

## Project structure

- `MainPage.xaml` - login, dashboard, inventory form/table, and audit interface
- `MainPage.xaml.cs` - navigation, validation, CRUD, persistence, and audit logic
- `Models/InventoryItem.cs` - inventory data model and chart value
- `Models/AuditEntry.cs` - audit record model
- `Resources/` - app icons, splash screen, fonts, and styles
- `output/docx/` - editable Word classroom submission document

## Notes

- Product and audit data are saved in `FileSystem.AppDataDirectory`.
- Four sample products are created the first time the app starts.
- The code intentionally uses clear code-behind so it is easy to discuss in a student presentation.
- Unlock the application with username `admin` and password `admin123`.

## Credits

Developed by **Arjunren Valdez**.

## License

Licensed under the MIT License. See `LICENSE`.
