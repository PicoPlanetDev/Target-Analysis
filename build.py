from pathlib import Path
import subprocess
import os

def main():
    # Get the path to the current directory
    current_dir = Path(__file__).parent.absolute()

    # Ask the user for the Path to the build directory
    repo_dir = input("Enter the path to the build directory (empty for parent folder): ")
    if repo_dir == "":
        repo_dir = Path(current_dir.parent, "Target-Analysis-build")
    else:
        repo_dir = Path(repo_dir)
    
    # Clone the repository into the build directory
    print(f"Cloning repository into {repo_dir}...")
    subprocess.run(["git", "clone", "https://github.com/PicoPlanetDev/Target-Analysis", str(repo_dir)])
    print(f"Repository cloned into {repo_dir}")

    # Build with pyinstaller
    print("Building with PyInstaller...")
    subprocess.run(["pyinstaller", "gui.spec"], cwd=repo_dir)
    print("Build complete")
    build_dir = Path(repo_dir, "dist", "TargetAnalysis")
    print(f"Binaries in {build_dir}")

    if os.name == "nt":
        # Ask the user if they want to hide files
        hide_files = input("Hide obscure files? (y/n): ")
        if hide_files == "y":
            exclude_paths = [
                "README.md",
                "LICENSE.md",
                "TargetAnalysis.exe",
                "data",
                "images"
            ]
            for path in build_dir.iterdir():
                name = Path(path).name
                if name not in exclude_paths:
                    subprocess.run(["attrib", "+h", name], cwd=build_dir)
            print("Files hidden")

        # Ask the user if they want to open the build directory in explorer
        open_explorer = input("Open build directory? (y/n): ")
        if open_explorer == "y":
            subprocess.run(["explorer", str(build_dir)])
        
    # Ask the user if they want to zip the build directory
    zip_build = input("Zip build directory? (y/n): ")
    if zip_build == "y":
        zip_path = Path(repo_dir, "Target-Analysis.zip")
        subprocess.run(["7z", "a", str(zip_path), str(build_dir)])
        print(f"Build zipped to {zip_path}")

if __name__ == "__main__":
    main()