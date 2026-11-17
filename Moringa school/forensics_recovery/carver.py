import os
import sys
import hashlib

# Predefined standard magic numbers for carving operations
FILE_SIGNATURES = {
    "jpg": {
        "header": b"\xff\xd8\xff",
        "footer": b"\xff\xd9"
    },
    "png": {
        "header": b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a",
        "footer": b"\x49\x45\x4e\x4d\x41\x4e\x44\xae\x42\x60\x82"
    },
    "pdf": {
        "header": b"\x25\x50\x44\x46",
        "footer": b"\x25\x25\x45\x4f\x46"
    }
}

def calculate_md5_hash(file_path):
    """Calculates an MD5 signature tracking structural validity."""
    md5_hasher = hashlib.md5()
    with open(file_path, "rb") as target_file:
        while chunk := target_file.read(4096):
            md5_hasher.update(chunk)
    return md5_hasher.hexdigest()

def process_disk_carving(image_path, output_directory):
    """Scans a raw binary data image to extract whole hidden files."""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    print(f"[*] Initializing carving process on target asset: {image_path}")
    
    try:
        with open(image_path, "rb") as image_file:
            raw_binary_stream = image_file.read()
    except Exception as e:
        print(f"[-] Critical Error reading target image: {e}")
        sys.exit(1)

    hash_registry = []
    file_sequence_id = 1

    for extension, markers in FILE_SIGNATURES.items():
        start_header_bytes = markers["header"]
        end_footer_bytes = markers["footer"]
        
        search_pointer = 0
        while True:
            header_offset = raw_binary_stream.find(start_header_bytes, search_pointer)
            if header_offset == -1:
                break 
            
            footer_offset = raw_binary_stream.find(end_footer_bytes, header_offset)
            if footer_offset != -1:
                end_offset = footer_offset + len(end_footer_bytes)
                computed_file_size = end_offset - header_offset
                
                extracted_payload = raw_binary_stream[header_offset:end_offset]
                filename = f"recovered_item_{file_sequence_id}.{extension}"
                destination_path = os.path.join(output_directory, filename)
                
                with open(destination_path, "wb") as output_file:
                    output_file.write(extracted_payload)
                
                md5_hash_value = calculate_md5_hash(destination_path)
                hash_registry.append(f"{md5_hash_value}  {filename}\n")
                
                print(f"[+] Identified: {extension.upper()} | Offset: {hex(header_offset)} | Size: {computed_file_size} bytes -> {filename}")
                
                file_sequence_id += 1
                search_pointer = end_offset  
            else:
                search_pointer = header_offset + len(start_header_bytes)

    log_file_path = os.path.join(output_directory, "hashes.txt")
    with open(log_file_path, "w", encoding="utf-8") as file_logger:
        file_logger.writelines(hash_registry)
        
    print(f"[+] Output telemetry logging written to: {log_file_path}")

def main():
    # Fallback default path if run directly inside the editor GUI interface
    target_image = sys.argv[1] if len(sys.argv) > 1 else "carveit"
    assigned_folder = "Mathenge"
    
    process_disk_carving(target_image, assigned_folder)

if __name__ == "__main__":
    main()