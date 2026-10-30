import openpyxl

EXCEL_FILE = "Assets/levels.xlsx"  
SHEET_NAME = "test"                  
OUTPUT_FILE = "Scripts/Map.py"             

COLORS = {
    "FFFFFFFF": ".",     
    "FF7F7F7F": "H",     
    "FF70AD47": "1",#ghoul
    "FFFBE5D5": "P",#start
    "FF7F6000": "R",#book shelf
    "FFBF9000": "R",#rare chest
    "FF335593": "2",#gargulye  
    "FFDEEBF6": ".",#barier
    "FFFFFF00": "M",#merchan
    "FFFF0000": "E",#level end
    "FFFFC000": "R",#chest
    "FF7030A0": "R"#pedestal
}

def color_to_symbol(fill):
    if fill is None:
        return "."
    if fill.patternType is None:
        return "."
    
    color = fill.start_color
    if color is None:
        return "." 
    
    if hasattr(color, 'theme') and color.theme is not None:
        theme_colors = {
            0: (255, 255, 255),
            1: (0, 0, 0),      
            2: (230, 230, 230),
            3: (166, 166, 166), 
            4: (68, 114, 196), 
            5: (237, 125, 49),  
            6: (165, 165, 165),  
            7: (255, 192, 0),    
            8: (91, 155, 213),   
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
        
        hex_color = f"FF{r:02X}{g:02X}{b:02X}"
        
        if hex_color not in COLORS:
            print(f"Неизвестный цвет (theme={getattr(color, 'theme', None)}, tint={getattr(color, 'tint', 0)}, hex={hex_color})")
        
        return COLORS.get(hex_color, "?")
    
    return "?"

def convert_excel_to_map():
    wb = openpyxl.load_workbook(EXCEL_FILE)
    sheet = wb[SHEET_NAME] if SHEET_NAME else wb.active
    
    lines = []
    for row in sheet.iter_rows():
        line = ""
        for cell in row:
            line += color_to_symbol(cell.fill)
        lines.append(line)
    
    output = "drawed_map = [\n"
    for line in lines:
        output += f'    "{line}",\n'
    output += "]\n"
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(output)

convert_excel_to_map()