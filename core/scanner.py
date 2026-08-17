from pathlib import Path


class FolderScanner:

    IMAGE_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".webp",
        ".tiff",
        ".svg",
    }

    VIDEO_EXTENSIONS = {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"}

    DOCUMENT_EXTENSIONS = {
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".txt",
        ".csv",
    }

    AUDIO_EXTENSIONS = {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"}

    ARCHIVE_EXTENSIONS = {".zip", ".rar", ".7z", ".tar", ".gz"}

    def scan(self, folder_path: str):

        folder = Path(folder_path)

        stats = {
            "total_files": 0,
            "total_folders": 0,
            "total_size": 0,
            "images": {},
            "videos": {},
            "documents": {},
            "audio": {},
            "archives": {},
            "others": {},
            "no_extension": {},
        }

        for item in folder.rglob("*"):

            if item.is_dir():
                stats["total_folders"] += 1
                continue

            stats["total_files"] += 1
            stats["total_size"] += item.stat().st_size

            extension = item.suffix.lower()

            if not extension:
                category = "no_extension"
                extension = "no_extension"
            else:
                extension = extension[1:]

                if f".{extension}" in self.IMAGE_EXTENSIONS:
                    category = "images"

                elif f".{extension}" in self.VIDEO_EXTENSIONS:
                    category = "videos"

                elif f".{extension}" in self.DOCUMENT_EXTENSIONS:
                    category = "documents"

                elif f".{extension}" in self.AUDIO_EXTENSIONS:
                    category = "audio"

                elif f".{extension}" in self.ARCHIVE_EXTENSIONS:
                    category = "archives"
                else:
                    category = "others"

            stats[category][extension] = stats[category].get(extension, 0) + 1

        # Remove empty categories
        empty_categories = []

        for category in [
            "images",
            "videos",
            "documents",
            "audio",
            "archives",
            "others",
            "no_extension",
        ]:
            if not stats[category]:
                empty_categories.append(category)

        for category in empty_categories:
            del stats[category]

        return stats
