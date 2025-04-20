from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name
from PIL import Image, ImageDraw, ImageFilter
from io import BytesIO

def detect_language(code):
    code = code.lower()
    patterns = {
        "python": ["def ", "import ", "print(", "self", "lambda ", "class "],
        "cpp": ["#include", "int main", "std::cout", "cin", "namespace", "using namespace", "class "],
        "javascript": ["function ", "console.log", "var ", "let ", "const ", "document.", "window."],
        "java": ["public class", "System.out.println", "void main", "import "],
        "c": ["#include", "int main", "printf", "scanf", "return "],
        "c#": ["using System", "public class", "Console.WriteLine", "namespace", "void Main"],
        "ruby": ["def ", "end", "puts ", "class ", "require"],
        "php": ["<?php", "echo ", "$_POST", "$_GET", "function ", "$this", "public function"],
        "swift": ["import Swift", "func ", "let ", "var ", "class "],
        "go": ["package main", "func main", "import ", "fmt.Println", "var "],
        "rust": ["fn main", "let ", "pub ", "impl ", "use ", "match "],
        "kotlin": ["fun main(", "val ", "var ", "println(", "package "],
        "typescript": ["function ", "console.log", "let ", "const ", "import ", "export"],
        "perl": ["sub ", "print ", "$", "$ARGV", "my "],
        "objective-c": ["@interface", "@implementation", "NSString", "int main", "NSLog"],
        "dart": ["import 'dart:", "void main", "class ", "print("],
        "scala": ["object ", "def main", "val ", "var ", "extends "],
        "lua": ["function ", "local ", "end", "print("],
        "html": ["<html>", "<body>", "<div>", "<head>", "<html>", "<title>"],
        "json": ["{", "}", "\"", ":"],
        "sql": ["select ", "insert into", "update ", "delete from", "from", "where"],
        "r": ["library(", "data.frame", "plot(", "install.packages"],
        "matlab": ["function ", "disp(", "end", "subplot", "plot"],
        "bash": ["#!/bin/bash", "echo ", "exit", "if", "then", "fi", "for", "done"],
        "powershell": ["Write-Host", "$", "Get-Command", "function ", "if", "else"],
        "plaintext": ["text", "plain", "file", "content", "read"]
    }
    for lang, keywords in patterns.items():
        if any(keyword in code for keyword in keywords):
            return lang
    return "text"

def image_generate(code, moddle='gruvbox-dark', name='code', lang=None):
    try:
        code_lang = detect_language(code)
        lexer = get_lexer_by_name(code_lang)
        style = get_style_by_name(moddle)
        formatter = ImageFormatter(
            font_name="font.ttf",
            style=style,
            line_numbers=True,
            line_number_bg="#2b2b2b",
            line_number_fg="#aaaaaa",
            image_pad=30,
            line_pad=10,
            font_size=32,
            dpi=1200,
        )
        raw_image = BytesIO()
        highlight(code, lexer, formatter, raw_image)
        raw_image.seek(0)
        with Image.open(raw_image) as img:
            img = img.convert("RGBA")
            code_width, code_height = img.size

            padding_width = 200
            padding_height = 200
            background_width = code_width + padding_width
            background_height = code_height + padding_height
            background = Image.new("RGBA", (background_width, background_height), (169, 169, 169))
            x_offset = (background_width - code_width) // 2
            y_offset = (background_height - code_height) // 2

            mask = Image.new("L", (code_width, code_height), 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle([(0, 0), (code_width, code_height)], radius=30, fill=255)
            img.putalpha(mask)
            background.paste(img, (x_offset, y_offset), mask=img)

            background = background.filter(ImageFilter.GaussianBlur(radius=15))
            background.paste(img, (x_offset, y_offset), mask=img) 

            final_image = BytesIO()
            background.save(final_image, format="PNG", quality=100)
            final_image.seek(0)
            with open(f"{name}.png", "wb") as f:
                f.write(final_image.read())
            return 'Done'
    except Exception as e:
        return f'Error: {e}'

