from pathlib import Path
import subprocess
import sys
import shutil


def build_frontend():
    frontend_dir = Path(__file__).parent / "frontend"
    if not frontend_dir.exists():
        print(f"Frontend directory not found at {frontend_dir}", file=sys.stderr)
        return

    print("Building frontend assets...")
    try:
        # Run npm install with error handling
        result = subprocess.run(
            ["npm", "install"],
            cwd=frontend_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            print(f"npm install failed: {result.stderr}", file=sys.stderr)
            raise Exception("npm install failed")

        # Run npm build with error handling
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=frontend_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            print(f"npm build failed: {result.stderr}", file=sys.stderr)
            raise Exception("npm build failed")

        # Copy the built assets
        copy_assets(frontend_dir)

    except subprocess.CalledProcessError as e:
        print(f"Failed to build frontend: {str(e)}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"Unexpected error building frontend: {str(e)}", file=sys.stderr)
        raise


def copy_assets(frontend_dir):
    dist_dir = frontend_dir / "dist"
    if not dist_dir.exists():
        raise Exception(f"Build directory not found at {dist_dir}")

    package_static_dir = Path(__file__).parent / "preswald" / "static"
    package_static_dir.mkdir(parents=True, exist_ok=True)

    # Copy dist contents
    print(f"Copying built assets to {package_static_dir}")
    for item in dist_dir.iterdir():
        dest = package_static_dir / item.name
        if dest.exists():
            if dest.is_dir():
                shutil.rmtree(dest)
            else:
                dest.unlink()
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    # Copy public assets
    public_dir = frontend_dir / "public"
    if public_dir.exists():
        print("Copying public assets...")
        for item in public_dir.iterdir():
            dest = package_static_dir / item.name
            if not dest.exists():
                if item.is_dir():
                    shutil.copytree(item, dest)
                else:
                    shutil.copy2(item, dest)


if __name__ == "__main__":
    build_frontend()
