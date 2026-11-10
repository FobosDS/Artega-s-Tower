import openpyxl

EXCEL_FILE = "Assets/levels.xlsx"  
SHEET_NAME = "test_room"                  
OUTPUT_FILE = "Scripts/Map.py"             

COLORS = {
    "FFFFFFFF": ".",    
    "FF7F7F7F": "O",     
    "FF385623": "1",#ghoul
    "FF335593": "2",#gargolye 
    "FFC00000": "3",#vampire
    "FF92D050": "M",#merchant
    "FF7030A0": "S",#pedestal
    "FFFFC000": "C",#chest
    "FFBF9000": "R",#rare chest
    "FFFF0000": "E",#level end
    "FFFBE5D5": "P",#start
    "FFDEEBF6": "J",#barier
    "FF7F6000": "A",#shelf
    "FF00B0F0": "F",#food
    "FFFFFF00": "G",#gold
    "FF002060": "D"#decoration
}

RARE_CHEST_NUMBERS = {
    "1": "r",
    "2": "s",
    "3": "t",
    "4": "u"
}

MERCHANT_NUMBERS = {
    "1": "m",
    "2": "n",
    "3": "o",
    "4": "p"
}

SHELF_NUMBERS = {
    "1": "A", "2": "B", "3": "H", "4": "I", "5": "K", "6": "L"
}

WALL_NUMBERS = {
    "1": "O", "2": "Q", "3": "N", "4": "T", "5": "U",
    "6": "V", "7": "W", "8": "X", "9": "Y"
}

def get_hex_from_color(color):
    if color is None:
        return None
    if hasattr(color, 'rgb') and isinstance(color.rgb, str):
        hex_color = color.rgb
        if hex_color == "00000000":
            return None
        if len(hex_color) == 6:
            hex_color = "FF" + hex_color
        return hex_color
    if hasattr(color, 'theme') and color.theme is not None:
        theme_colors = {
            0: (255, 255, 255), 1: (0, 0, 0), 2: (230, 230, 230),
            3: (166, 166, 166), 4: (68, 114, 196), 5: (237, 125, 49),
            6: (165, 165, 165), 7: (255, 192, 0), 8: (91, 155, 213),
            9: (112, 173, 71),
        }
        base = theme_colors.get(color.theme, (255, 255, 255))
        tint = color.tint if color.tint else 0.0
        if tint > 0:
            r = int(base[0] + (255 - base[0]) * tint)
            g = int(base[1] + (255 - base[1]) * tint)
            b = int(base[2] + (255 - base[2]) * tint)
        elif tint < 0:
            r = int(base[0] * (1 + tint))
            g = int(base[1] * (1 + tint))
            b = int(base[2] * (1 + tint))
        else:
            r, g, b = base
        return f"FF{r:02X}{g:02X}{b:02X}"
    return None

def color_to_symbol(fill, cell_value=None):
    if fill is None:
        return "."
    if fill.patternType is None:
        return "."
    
    color = fill.start_color
    if color is None:
        return "."
    
    hex_color = get_hex_from_color(color)
    if hex_color is None:
        return "."
    
    if hex_color in COLORS:
        symbol = COLORS[hex_color]
        
        value_str = None
        if cell_value is not None:
            value_str = str(cell_value).strip()
        
        if symbol == "A" and value_str in SHELF_NUMBERS:
            return SHELF_NUMBERS[value_str]
        
        if symbol == "O" and value_str in WALL_NUMBERS:
            return WALL_NUMBERS[value_str]

        if symbol == "R" and value_str in RARE_CHEST_NUMBERS:
            return RARE_CHEST_NUMBERS[value_str]

        if symbol == "M" and value_str in MERCHANT_NUMBERS:
            return MERCHANT_NUMBERS[value_str]
        
        return symbol
    
    print(f"Неизвестный цвет (theme={getattr(color, 'theme', None)}, tint={getattr(color, 'tint', 0)}, hex={hex_color})")
    return "?"

def convert_excel_to_map():
    wb = openpyxl.load_workbook(EXCEL_FILE)
    sheet = wb[SHEET_NAME] if SHEET_NAME else wb.active
    
    lines = []
    for row in sheet.iter_rows():
        line = ""
        for cell in row:
            line += color_to_symbol(cell.fill, cell.value)
        lines.append(line)
    
    output = "drawed_map = [\n"
    for line in lines:
        output += f'    "{line}",\n'
    output += "]\n"
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(output)

convert_excel_to_map()