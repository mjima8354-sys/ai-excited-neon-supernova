#!/usr/bin/env python3
"""
Make.fun Bounty Entry: ai-excited-01 (Neon Supernova)
Procedurally generates a stunning, high-quality 1024x1024 indexed-color neon supernova PNG
using pure Python standard library (no external dependencies).
"""

import os
import sys
import struct
import zlib
import math
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
        
    if file_size < 33:
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
        has_plte = False
        
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
            elif chunk_type == b"PLTE":
                has_plte = True
            elif chunk_type == b"IEND":
                has_iend = True
                
            chunk_index += 1
            
        if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
            print(f"Error: Expected dimensions {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}, got {width}x{height}.", file=sys.stderr)
            sys.exit(1)
            
        if not has_iend:
            print("Error: Missing IEND chunk.", file=sys.stderr)
            sys.exit(1)

def build_palette() -> list[tuple[int, int, int]]:
    """Build a 256-color palette containing deep space, nebula, neon rings, and core highlights."""
    palette = []
    # 0..63: Deep cosmic void to dark indigo/violet
    for i in range(64):
        t = i / 63.0
        r = int(2 + t * 20)
        g = int(1 + t * 10)
        b = int(8 + t * 50)
        palette.append((r, g, b))
        
    # 64..127: Nebula purple & hot magenta clouds
    for i in range(64):
        t = i / 63.0
        r = int(22 + t * 233)
        g = int(11 + t * 30)
        b = int(58 + t * 150)
        palette.append((r, g, b))
        
    # 128..191: Electric cyan & bright blue shockwave rings
    for i in range(64):
        t = i / 63.0
        r = int(255 - t * 200)
        g = int(41 + t * 190)
        b = int(208 + t * 47)
        palette.append((r, g, b))
        
    # 192..239: Golden orange / flame shockwaves
    for i in range(48):
        t = i / 47.0
        r = int(55 + t * 200)
        g = int(231 - t * 100)
        b = int(255 - t * 200)
        palette.append((r, g, b))
        
    # 240..255: Blinding white-hot core highlights
    for i in range(16):
        t = i / 15.0
        r = 255
        g = int(131 + t * 124)
        b = int(55 + t * 200)
        palette.append((r, g, b))
        
    return palette

def generate_neon_supernova_indexed(width: int, height: int, palette: list[tuple[int, int, int]]) -> bytes:
    """Procedurally render 1024x1024 neon supernova and map each pixel to a palette index (0-255)."""
    cx = width / 2.0
    cy = height / 2.0
    
    indices = bytearray(width * height)
    idx = 0
    max_r = math.hypot(cx, cy)
    
    for y in range(height):
        dy = y - cy
        for x in range(width):
            dx = x - cx
            r = math.hypot(dx, dy)
            angle = math.atan2(dy, dx)
            
            # Smooth nebula gas clouds
            n1 = math.sin(dx * 0.006 + math.cos(dy * 0.005))
            n2 = math.cos(dy * 0.007 - math.sin(dx * 0.006))
            n3 = math.sin(r * 0.004 - angle * 3.0)
            nebula = max(0.0, (n1 + n2 + n3 * 1.5) / 3.5)
            
            # Shockwave rings
            ring1 = math.exp(-((r - 190.0) ** 2) / 800.0) * (0.5 + 0.5 * math.sin(angle * 12.0 + r * 0.02))
            ring2 = math.exp(-((r - 350.0) ** 2) / 1400.0) * (0.5 + 0.5 * math.cos(angle * 16.0 - r * 0.03))
            ring3 = math.exp(-((r - 500.0) ** 2) / 2500.0) * (0.4 + 0.6 * math.sin(angle * 10.0))
            
            # Core & diffraction rays
            core = math.exp(-(r ** 2) / 18000.0) * 1.5
            core_bright = math.exp(-(r ** 2) / 1000.0) * 2.5
            flash = math.exp(-(r ** 2) / 200.0) * 4.0
            
            ray1 = abs(math.sin(angle * 4.0)) ** 24
            ray2 = abs(math.sin(angle * 4.0 + math.pi / 4.0)) ** 32
            rays = (ray1 * 1.5 + ray2 * 1.0) * math.exp(-r / 380.0) * max(0.0, 1.0 - r / 650.0)
            
            # Compute composite intensity / energy level (0.0 to 1.0+)
            energy = (1.0 - r / max_r) * 0.15 + nebula * 0.35 + ring1 * 0.4 + ring2 * 0.5 + ring3 * 0.3 + core * 0.3 + core_bright * 0.7 + rays * 0.6 + flash * 1.5
            
            # Map energy to palette index (0..255)
            if flash > 0.5:
                color_idx = 240 + int(min(1.0, (flash - 0.5) / 3.5) * 15)
            elif core_bright > 0.3 or rays > 0.3:
                color_idx = 192 + int(min(1.0, max(core_bright, rays) / 2.5) * 47)
            elif ring1 > 0.3 or ring2 > 0.3:
                color_idx = 128 + int(min(1.0, max(ring1, ring2) / 1.0) * 63)
            elif nebula > 0.2:
                color_idx = 64 + int(min(1.0, nebula / 1.2) * 63)
            else:
                color_idx = int(min(1.0, r / max_r) * 63)
                
            indices[idx] = min(255, max(0, color_idx))
            idx += 1
            
    return bytes(indices)

def create_png_indexed(width: int, height: int, palette: list[tuple[int, int, int]], pixel_indices: bytes) -> bytes:
    """Encode indexed pixels and palette into a valid PNG byte stream."""
    plte_data = bytearray()
    for rgb in palette:
        plte_data.extend(rgb)
        
    row_stride = width
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0)  # Filter type 0
        start = y * row_stride
        raw_data.extend(pixel_indices[start:start + row_stride])
        
    compressed = zlib.compress(raw_data, level=9)
    
    def chunk(c_type: bytes, c_data: bytes) -> bytes:
        return struct.pack(">I", len(c_data)) + c_type + c_data + struct.pack(">I", zlib.crc32(c_type + c_data) & 0xffffffff)

    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 3, 0, 0, 0)
    
    png_bytes = bytearray(b"\x89PNG\r\n\x1a\n")
    png_bytes.extend(chunk(b"IHDR", ihdr_data))
    png_bytes.extend(chunk(b"PLTE", bytes(plte_data)))
    png_bytes.extend(chunk(b"IDAT", compressed))
    png_bytes.extend(chunk(b"IEND", b""))
    return bytes(png_bytes)

def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(script_dir, "entry.png")
    
    print("Generating enhanced neon supernova 1024x1024 indexed image procedurally...")
    palette = build_palette()
    pixel_indices = generate_neon_supernova_indexed(EXPECTED_WIDTH, EXPECTED_HEIGHT, palette)
    png_data = create_png_indexed(EXPECTED_WIDTH, EXPECTED_HEIGHT, palette, pixel_indices)
    
    try:
        with open(src_path, "wb") as f:
            f.write(png_data)
    except Exception as e:
        print(f"Note: could not write entry.png in repo dir ({e}); continuing", file=sys.stderr)
    try:
        validate_png(src_path)
    except SystemExit:
        pass

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except Exception as e:
        print(f"Error: cannot create output dir {out_dir}: {e}", file=sys.stderr)
        sys.exit(1)

    dest_path = os.path.join(out_dir, "entry.png")

    dir_name = os.path.dirname(dest_path)
    try:
        fd, temp_path = tempfile.mkstemp(dir=dir_name, prefix=".entry_tmp_", suffix=".png")
    except Exception as e:
        print(f"Error: cannot create temp file in {dir_name}: {e}", file=sys.stderr)
        sys.exit(1)
    try:
        with os.fdopen(fd, "wb") as temp_f:
            temp_f.write(png_data)
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
        
    validate_png(dest_path)
    
    print(f"Successfully generated, validated, and copied neon supernova entry.png to {dest_path}")

if __name__ == "__main__":
    main()
