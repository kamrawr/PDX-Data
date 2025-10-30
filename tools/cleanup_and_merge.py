import os
import pandas as pd
import glob
from datetime import datetime

print("🧹 Cleaning up and organizing PDX assessor data...\n")

# Remove old generic files
old_files = glob.glob("downloads/Assessor-Search-Results*.csv")
if old_files:
    print(f"Removing {len(old_files)} old generic download files...")
    for f in old_files:
        os.remove(f)
        
# Get all properly named neighborhood files
neighborhood_files = [f for f in glob.glob("downloads/*.csv") if "_page" in f]
print(f"Found {len(neighborhood_files)} neighborhood data files\n")

# Organize by neighborhood
neighborhoods = {}
for filepath in neighborhood_files:
    filename = os.path.basename(filepath)
    neighborhood = filename.split("_page")[0]
    
    if neighborhood not in neighborhoods:
        neighborhoods[neighborhood] = []
    neighborhoods[neighborhood].append(filepath)

print(f"📊 Data Summary:")
print(f"Total neighborhoods: {len(neighborhoods)}")
multi_page = {n: len(files) for n, files in neighborhoods.items() if len(files) > 1}
if multi_page:
    print(f"Multi-page neighborhoods: {len(multi_page)}")
    for n, count in sorted(multi_page.items())[:10]:
        print(f"  - {n}: {count} pages")
    if len(multi_page) > 10:
        print(f"  ... and {len(multi_page) - 10} more")

# Merge all data
print("\n📦 Merging all neighborhood data...")
all_frames = []

for neighborhood, files in sorted(neighborhoods.items()):
    print(f"  Processing {neighborhood}...")
    for filepath in sorted(files):
        try:
            df = pd.read_csv(filepath)
            df["neighborhood"] = neighborhood
            df["source_file"] = os.path.basename(filepath)
            all_frames.append(df)
        except Exception as e:
            print(f"    ⚠️  Error reading {filepath}: {e}")

# Combine all data
print("\n🔗 Combining data...")
combined = pd.concat(all_frames, ignore_index=True)

# Remove duplicates (in case of overlapping downloads)
initial_rows = len(combined)
combined = combined.drop_duplicates()
final_rows = len(combined)
if initial_rows > final_rows:
    print(f"   Removed {initial_rows - final_rows} duplicate rows")

# Save combined file
output_file = "Portland_Assessor_AllNeighborhoods.csv"
combined.to_csv(output_file, index=False)
print(f"\n✅ Combined dataset saved: {output_file}")
print(f"   Total rows: {len(combined):,}")
print(f"   Total columns: {len(combined.columns)}")

# Create summary report
summary_file = "data_summary.txt"
with open(summary_file, "w") as f:
    f.write("Portland Assessor Data Collection Summary\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Collection Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Total Properties: {len(combined):,}\n")
    f.write(f"Total Neighborhoods: {len(neighborhoods)}\n")
    f.write(f"Total Files Processed: {len(neighborhood_files)}\n\n")
    
    f.write("Properties by Neighborhood:\n")
    f.write("-" * 50 + "\n")
    neighborhood_counts = combined.groupby('neighborhood').size().sort_values(ascending=False)
    for hood, count in neighborhood_counts.items():
        f.write(f"{hood}: {count:,}\n")

print(f"📝 Summary report saved: {summary_file}")

# Create a clean data folder
print("\n📁 Organizing files...")
os.makedirs("raw_downloads", exist_ok=True)

for f in neighborhood_files:
    new_path = f.replace("downloads/", "raw_downloads/")
    os.rename(f, new_path)

print(f"   Moved {len(neighborhood_files)} files to raw_downloads/")

print("\n🎉 All done! Your data is ready.")
print(f"\nMain dataset: {output_file}")
print(f"Raw files: raw_downloads/")
print(f"Summary: {summary_file}")
