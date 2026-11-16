#!/usr/bin/env python3
"""
Make.fun Bounty Entry: ai-excited-01
Validates and deterministically copies entry.png.
"""

import os
import sys
import struct
import zlib
import tempfile

MAX_FILE_SIZE = 1024 * 1024  # 1 MiB
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

def validate_png(file_path: str) -> None:
    """Rigorously validate PNG file structure, size, dimensions, and chunk CRCs."""
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
        
    file_size = os.path.getsize(file_path)
    if file_size >= MAX_FILE_SIZE:
        print(f"Error: File size ({file_size} bytes) exceeds 1 MiB limit.", file=sys.stderr)
        sys.exit(1)
        
    if file_size < 33:  # Minimum PNG size (signature + IHDR + IEND)
        print(f"Error: File size ({file_size} bytes) is too small for a valid PNG.", file=sys.stderr)
        sys.exit(1)

    with open(file_path, "rb") as f:
        signature = f.read(8)
        if signature != PNG_SIGNATURE:
            print("Error: Invalid PNG signature.", file=sys.stderr)
            sys.exit(1)
            
        chunk_index = 0
        width, height = None, None
        has_iend = False
        
        while True:
            length_bytes = f.read(4)
            if not length_bytes:
                break
            if len(length_bytes) != 4:
                print("Error: Unexpected EOF while reading chunk length.", file=sys.stderr)
                sys.exit(1)
                
            length = struct.unpack(">I", length_bytes)[0]
            if length > 0x7fffffff:
                print("Error: Invalid chunk length.", file=sys.stderr)
                sys.exit(1)
                
            chunk_type = f.read(4)
            if len(chunk_type) != 4 or not all(65 <= b <= 90 or 97 <= b <= 122 for b in chunk_type):
                print("Error: Invalid or malformed chunk type.", file=sys.stderr)
                sys.exit(1)
                
            data = f.read(length)
            if len(data) != length:
                print("Error: Unexpected EOF while reading chunk data.", file=sys.stderr)
                sys.exit(1)
                
            crc_bytes = f.read(4)
            if len(crc_bytes) != 4:
                print("Error: Unexpected EOF while reading chunk CRC.", file=sys.stderr)
                sys.exit(1)
                
            stored_crc = struct.unpack(">I", crc_bytes)[0]
            computed_crc = zlib.crc32(chunk_type + data) & 0xffffffff
            if computed_crc != stored_crc:
                print(f"Error: CRC mismatch in chunk {chunk_type.decode('ascii', errors='replace')}.", file=sys.stderr)
                sys.exit(1)
                
            # Chunk validation rules
            if chunk_index == 0:
                if chunk_type != b"IHDR":
                    print("Error: First chunk must be IHDR.", file=sys.stderr)
                    sys.exit(1)
            
            if chunk_type == b"IHDR":
                if length != 13:
                    print("Error: Invalid IHDR length.", file=sys.stderr)
                    sys.exit(1)
                width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack(">IIBBBBB", data)
                if bit_depth not in (8, 16):
                    print(f"Error: Unsupported bit depth: {bit_depth}.", file=sys.stderr)
                    sys.exit(1)
                if color_type not in (0, 2, 3, 4, 6):
                    print(f"Error: Unsupported color type: {color_type}.", file=sys.stderr)
                    sys.exit(1)
                if compression != 0 or filter_method != 0 or interlace not in (0, 1):
                    print("Error: Invalid compression, filter, or interlace method in IHDR.", file=sys.stderr)
                    sys.exit(1)
            elif chunk_type == b"IEND":
                has_iend = True
                
            chunk_index += 1
            
        if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
            print(f"Error: Expected dimensions {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}, got {width}x{height}.", file=sys.stderr)
            sys.exit(1)
            
        if not has_iend:
            print("Error: Missing IEND chunk.", file=sys.stderr)
            sys.exit(1)

def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(script_dir, "entry.png")
    
    # Validate source image thoroughly
    validate_png(src_path)
    
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    
    dest_path = os.path.join(out_dir, "entry.png")
    
    # Read source content deterministically
    with open(src_path, "rb") as src_f:
        content = src_f.read()
        
    # Atomic write using temporary file in target directory
    dir_name = os.path.dirname(dest_path)
    fd, temp_path = tempfile.mkstemp(dir=dir_name, prefix=".entry_tmp_", suffix=".png")
    try:
        with os.fdopen(fd, "wb") as temp_f:
            temp_f.write(content)
            temp_f.flush()
            os.fsync(temp_f.fileno())
        os.replace(temp_path, dest_path)
    except Exception as e:
        if os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except Exception:
                pass
        print(f"Error during atomic write: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Verify destination file as well
    validate_png(dest_path)
    
    print(f"Successfully hardened, validated, and copied entry.png to {dest_path}")

if __name__ == "__main__":
    main()
