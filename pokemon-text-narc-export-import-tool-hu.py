#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pokemon-text-narc-export-import-tool-hu.py
Pokémon B/W NARC szövegkezelő eszköz – Export és Import funkciókkal.
Ez a verzió magyar nyelvű.
"""

import argparse
import json
import struct
import sys
from pathlib import Path
from random import randint

# ---------- Segédfüggvények és alaposztályok ---------- #

def pad32(b: bytearray) -> None:
    """A bájt-tömböt 4-gyel osztható hosszúságúra egészíti ki."""
    while len(b) % 4:
        b += b'\xFF'

class DS:
    """Egyszerűsített DataStream a bináris adatok írásához és olvasásához."""
    def __init__(self, data=b''):
        self.d = bytearray(data)
        self.p = 0
    def w16(self, v): self.d += struct.pack('<H', v & 0xFFFF)
    def w32(self, v): self.d += struct.pack('<I', v & 0xFFFFFFFF)
    def w(self, b): self.d += b
    def r16(self): v, = struct.unpack_from('<H', self.d, self.p); self.p += 2; return v
    def r32(self): v, = struct.unpack_from('<I', self.d, self.p); self.p += 4; return v
    def seek(self, pos): self.p = pos
    def tell(self): return self.p
    def remaining(self): return len(self.d) - self.p

class NARC:
    """NARC archívumok beolvasására és újraépítésére szolgáló osztály."""
    def __init__(self):
        self.entries = []

    @classmethod
    def open(cls, fn: str):
        raw = Path(fn).read_bytes()
        if raw[0:4] != b'NARC': raise ValueError(f"'{fn}' nem érvényes NARC fájl.")
        btaf = raw.find(b'BTAF')
        if btaf == -1: raise ValueError("Hiányzó BTAF blokk a NARC fájlban.")
        files = struct.unpack_from('<I', raw, btaf + 8)[0]
        offs = [struct.unpack_from('<II', raw, btaf + 12 + i*8) for i in range(files)]
        gmif = raw.find(b'GMIF')
        if gmif == -1: raise ValueError("Hiányzó GMIF blokk a NARC fájlban.")
        gmif_data_start = gmif + 8
        nar = cls()
        for s, e in offs: nar.entries.append(raw[gmif_data_start + s: gmif_data_start + e])
        return nar

    def rebuild(self, new_entries: list[bytes]) -> bytes:
        out = DS()
        out.w(b'NARC'); out.w16(0xFFFE); out.w16(0x0100); out.w32(0); out.w16(0x10); out.w16(3)
        btaf_start = len(out.d); out.w(b'BTAF'); out.w32(0); out.w32(len(new_entries))
        cur = 0
        for e in new_entries:
            out.w32(cur); cur += len(e); out.w32(cur)
        out.w(b'BTNF'); out.w32(0x10); out.w32(4); out.w16(0x10000); out.w16(1)
        gmif_start = len(out.d); out.w(b'GMIF'); out.w32(0)
        for e in new_entries: out.w(e)
        pad32(out.d)
        total = len(out.d)
        struct.pack_into('<I', out.d, 8, total)
        struct.pack_into('<I', out.d, btaf_start + 4, gmif_start - btaf_start)
        struct.pack_into('<I', out.d, gmif_start + 4, total - gmif_start)
        return bytes(out.d)

# ---------- Szöveg Kódolás (IMPORT) és Dekódolás (EXPORT) ---------- #

class TxtCodec:
    INIT_KEY = 0x1234

    @staticmethod
    def get_strings(data: bytes) -> list[str]:
        if len(data) < 12: return []
        ds = DS(data)
        try:
            ds.seek(2); num_entries = ds.r16(); ds.seek(12)
            section_offset = ds.r32()
            if section_offset >= len(data): return []
            ds.seek(section_offset); ds.r32()
            table = []
            for _ in range(num_entries):
                if ds.remaining() < 8: break
                table.append({'offset': ds.r32(), 'count': ds.r16()})
                ds.seek(ds.tell() + 2)
            strings = []
            for entry in table:
                text_start = section_offset + entry['offset']
                if text_start + (entry['count'] * 2) > len(data): continue
                ds.seek(text_start)
                enc_chars = [ds.r16() for _ in range(entry['count'])]
                if not enc_chars:
                    strings.append(""); continue
                key = enc_chars[-1] ^ 0xFFFF
                for k in range(len(enc_chars) - 1, -1, -1):
                    enc_chars[k] ^= key
                    if k > 0: key = ((key >> 3) | (key << 13)) & 0xFFFF
                decoded_str = "".join(chr(c) if 0x20 <= c <= 0xFFF0 and c != 0xF000 and not (0xD800 <= c <= 0xDFFF) else f"\\x{c:04x}" for c in enc_chars if c != 0xFFFF)
                strings.append(decoded_str)
            return strings
        except (IndexError, struct.error): return []

    @staticmethod
    def txt_to_codes(txt: str) -> list[int]:
        codes, i = [], 0
        while i < len(txt):
            if txt[i:i+2] == '\\x' and i+5 < len(txt):
                try:
                    codes.append(int(txt[i+2:i+6], 16) & 0xFFFF); i += 6; continue
                except ValueError: pass
            codes.append(ord(txt[i]) & 0xFFFF); i += 1
        return codes

    @classmethod
    def encrypt(cls, codes: list[int]) -> bytes:
        if not codes: return b''
        k = cls.INIT_KEY; keys = {}
        for idx in range(len(codes), -1, -1):
            keys[idx] = k
            if idx: k = ((k >> 3) | (k << 13)) & 0xFFFF
        enc = [(c ^ keys[i]) & 0xFFFF for i, c in enumerate(codes)]
        enc.append(cls.INIT_KEY ^ 0xFFFF)
        return struct.pack(f'<{len(enc)}H', *enc)

    @classmethod
    def build_entry(cls, texts: list[str]) -> bytes:
        chunks = [cls.encrypt(cls.txt_to_codes(t)) for t in texts]
        section_builder = DS(); section_builder.w32(0)
        offset = 4 + len(texts) * 8
        for chunk in chunks:
            section_builder.w32(offset); section_builder.w16(len(chunk) // 2); section_builder.w16(0x0100)
            offset += len(chunk)
        for chunk in chunks: section_builder.w(chunk)
        struct.pack_into('<I', section_builder.d, 0, len(section_builder.d))
        entry_header = DS()
        entry_header.w16(1); entry_header.w16(len(texts)); entry_header.w32(len(section_builder.d))
        entry_header.w32(0); entry_header.w32(16)
        return bytes(entry_header.d + section_builder.d)

# ---------- Export és Import segédfüggvények ---------- #

def export_to_json(narc: NARC, json_path: str):
    data = {'entries': [{'entry_index': i, 'texts': [{'text_index': j, 'original_text': t, 'translated_text': t} for j, t in enumerate(TxtCodec.get_strings(b))]} for i, b in enumerate(narc.entries)]}
    with open(json_path, 'w', encoding='utf-8', errors='surrogatepass') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[SIKER] Exportálás befejezve: {json_path}")

def export_to_directory(narc: NARC, dir_path: str):
    p = Path(dir_path); p.mkdir(exist_ok=True)
    lang_dir = p / "0000"; lang_dir.mkdir(exist_ok=True)
    count = 0
    for i, entry_bytes in enumerate(narc.entries):
        texts = TxtCodec.get_strings(entry_bytes)
        if not texts: continue
        with open(lang_dir / f"{i:04d}.txt", 'w', encoding='utf-8', errors='surrogatepass') as f:
            f.write(f"# Bejegyzés {i:04d}\n\n")
            for j, text in enumerate(texts): f.write(f"[{j:04d}]\n{text}\n\n")
        count += 1
    print(f"[SIKER] {count} bejegyzés exportálva a(z) '{dir_path}' mappába.")

def load_translations(source_path: str, num_entries: int) -> list[list[str]]:
    p = Path(source_path)
    if p.is_dir():
        lang_dir = p / "0000"
        if not lang_dir.is_dir(): raise FileNotFoundError(f"A '{lang_dir}' mappa nem található.")
        all_translations = [[] for _ in range(num_entries)]
        for i in range(num_entries):
            fpath = lang_dir / f"{i:04d}.txt"
            if not fpath.exists(): continue
            with open(fpath, 'r', encoding='utf-8', errors='surrogatepass') as f: content = f.read()
            texts = {}
            current_idx, current_text = -1, ""
            for line in content.splitlines():
                if line.startswith('[') and line.endswith(']'):
                    if current_idx != -1: texts[current_idx] = current_text.strip()
                    try: current_idx = int(line[1:-1]); current_text = ""
                    except ValueError: current_idx = -1
                elif not line.startswith('#') and current_idx != -1: current_text += line + '\n'
            if current_idx != -1: texts[current_idx] = current_text.strip()
            if texts: all_translations[i] = [texts.get(j, "") for j in range(max(texts.keys()) + 1)]
        return all_translations
    elif p.is_file():
        with open(p, encoding='utf-8', errors='surrogatepass') as f: data = json.load(f)
        return [[t.get('translated_text') or '' for t in e.get('texts', [])] for e in (data['entries'] if isinstance(data, dict) else data)]
    else: raise FileNotFoundError("A megadott bemeneti forrás nem létezik.")

# ---------- Önellenőrzés és Főprogram ---------- #

def selftest():
    s = ''.join(chr(randint(0x20, 0x7E)) for _ in range(10))
    entry = TxtCodec.build_entry([s])
    decrypted = TxtCodec.get_strings(entry)
    assert len(decrypted) == 1 and decrypted[0] == s, 'Önteszt sikertelen!'
    print('[ÖNTESZT] Kódolási/dekódolási algoritmus helyes.')

def main():
    parser = argparse.ArgumentParser(description='Pokémon B/W NARC szövegkezelő eszköz (Export/Import)', formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest='command', help='Elérhető parancsok')

    p_export = subparsers.add_parser('export', help='Szövegek exportálása NARC fájlból.', epilog="Példák:\n  python %(prog)s export a003.narc -o szovegek.json\n  python %(prog)s export a003.narc -d forditando_szovegek")
    p_export.add_argument('input_narc', help='A bemeneti NARC fájl.')
    p_export.add_argument('-o', '--output-json', help='A kimeneti JSON fájl neve.')
    p_export.add_argument('-d', '--output-dir', help='Kimeneti mappa .txt fájlokhoz.')

    p_import = subparsers.add_parser('import', help='Szövegek visszaimportálása NARC fájlba.', epilog="Példák:\n  python %(prog)s import szovegek.json a003.narc uj.narc\n  python %(prog)s import forditott_szovegek/ a003.narc uj.narc")
    p_import.add_argument('input_source', help='Bemeneti forrás (JSON fájl vagy mappa).')
    p_import.add_argument('narc_original', help='Az eredeti NARC fájl.')
    p_import.add_argument('narc_output', help='A kimeneti, új NARC fájl neve.')
    
    if len(sys.argv) == 1:
        parser.print_help(); sys.exit(0)

    args = parser.parse_args()

    try:
        selftest()
        if args.command == 'export':
            if not args.output_json and not args.output_dir: p_export.error("Legalább egy kimenetet meg kell adni (-o vagy -d).")
            narc = NARC.open(args.input_narc)
            if args.output_json: export_to_json(narc, args.output_json)
            if args.output_dir: export_to_directory(narc, args.output_dir)
        elif args.command == 'import':
            narc = NARC.open(args.narc_original)
            translations = load_translations(args.input_source, len(narc.entries))
            if len(translations) != len(narc.entries): print(f"[FIGYELEM] Bejegyzések száma eltér: forrás ({len(translations)}) vs. NARC ({len(narc.entries)}).")
            new_entries, count = [], 0
            for i, original in enumerate(narc.entries):
                if i < len(translations) and any(translations[i]):
                    new_entries.append(TxtCodec.build_entry(translations[i])); count += 1
                else: new_entries.append(original)
            print(f"[INFO] {count} bejegyzés frissítve.")
            Path(args.narc_output).write_bytes(narc.rebuild(new_entries))
            print(f"[SIKER] Importálás befejezve! Az új fájl: {args.narc_output}")
    except Exception as ex:
        print(f'[HIBA] {ex}', file=sys.stderr); sys.exit(1)

if __name__ == '__main__':
    main()
