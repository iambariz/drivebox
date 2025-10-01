from typing import Optional, Dict
from drivebox.auth import get_gdrive_service, delete_token


class GoogleDriveAuthService:
    """Handles Google Drive authentication."""
    
    def login(self) -> Optional[Dict[str, str]]:
        """
        Authenticate user with Google Drive.
        
        Returns:
            Dict with 'name' and 'email' if successful, None otherwise
        """
        service = get_gdrive_service()
        if service:
            about = service.about().get(fields="user").execute()
            user = about["user"]
            return {
                "name": user["displayName"],
                "email": user["emailAddress"]
            }
        return None
    
    def logout(self) -> None:
        """Remove authentication token."""
        delete_token()