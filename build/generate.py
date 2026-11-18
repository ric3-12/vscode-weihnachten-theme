"""Erzeugt die drei Theme-Dateien aus Farbpaletten und prüft die Kontraste."""
import json, os, sys

PALETTES = {
    "tannengruen": dict(
        label="Weihnachten Tannengrün", kind="dark",
        bg="#0f1c14", bg2="#0d1912", bg3="#0a130e", border="#1a2e21", hl="#15281c", hover="#16291d",
        fg="#e9efe9", fg2="#cfdad1", muted="#7f9585", comment="#6b8a76", lineNr="#3f5c48",
        accent="#c4302b", accentHover="#e03a34", accentFg="#ffffff", gold="#f2c14e",
        keyword="#ff6b61", string="#7ee08a", number="#f2c14e", function="#8fd3ff",
        type="#ffb36b", param="#f5d9a8", tag="#ff6b61", attr="#f2c14e", op="#b9c9bd", regex="#7fdcd3",
        status="#0a130e", statusFg="#e9efe9", statusBorder="#c4302b",
        sel="#c4302b55", selInactive="#c4302b2a", find="#d4af3766", findHl="#d4af3733",
        ansi=dict(black="#0a130e", red="#ff4d4d", green="#3fd47a", yellow="#f2c14e", blue="#5eb0ff",
                  magenta="#e07ab8", cyan="#7fdcd3", white="#e9efe9"),
    ),
    "schnee": dict(
        label="Weihnachten Schnee", kind="light",
        bg="#fbfaf7", bg2="#f3f0e9", bg3="#ebe6dc", border="#ddd6c8", hl="#f2ede3", hover="#ece6da",
        fg="#24312a", fg2="#3b4740", muted="#6b766f", comment="#717d75", lineNr="#a9b1ab",
        accent="#b3261e", accentHover="#c8352c", accentFg="#ffffff", gold="#9a6a00",
        keyword="#b3261e", string="#1d7039", number="#8a5d00", function="#1f5f99",
        type="#a3480f", param="#6d4c1f", tag="#b3261e", attr="#8a5d00", op="#4f5a53", regex="#16707a",
        status="#b3261e", statusFg="#ffffff", statusBorder="#b3261e",
        sel="#b3261e26", selInactive="#b3261e14", find="#e0b84a80", findHl="#e0b84a40",
        ansi=dict(black="#24312a", red="#b3261e", green="#1d7039", yellow="#8a5d00", blue="#1f5f99",
                  magenta="#9b3d7a", cyan="#16707a", white="#6b766f"),
    ),
    "lebkuchen": dict(
        label="Weihnachten Lebkuchen", kind="dark",
        bg="#2a1d15", bg2="#24180f", bg3="#1d130c", border="#3b2a1e", hl="#33241a", hover="#33241a",
        fg="#f3e6d3", fg2="#e2d2bb", muted="#a88f78", comment="#9a8068", lineNr="#6a5442",
        accent="#d9603b", accentHover="#e8734d", accentFg="#1d130c", gold="#f2b45a",
        keyword="#f08a6c", string="#bfd68a", number="#f2b45a", function="#a9cdee",
        type="#e8a06b", param="#e8d3b0", tag="#f08a6c", attr="#f2b45a", op="#cdb79c", regex="#9fd3c0",
        status="#1d130c", statusFg="#f3e6d3", statusBorder="#d9603b",
        sel="#d9603b55", selInactive="#d9603b2a", find="#f2b45a66", findHl="#f2b45a33",
        ansi=dict(black="#1d130c", red="#f08a6c", green="#bfd68a", yellow="#f2b45a", blue="#9fc4e8",
                  magenta="#e0a0c0", cyan="#9fd3c0", white="#f3e6d3"),
    ),
}


def colors(p):
    a = p["ansi"]
    c = {
        "focusBorder": p["gold"], "foreground": p["fg"], "descriptionForeground": p["muted"],
        "disabledForeground": p["muted"] + "99", "errorForeground": p["keyword"],
        "icon.foreground": p["fg2"], "selection.background": p["sel"], "widget.shadow": "#00000040",
        "textLink.foreground": p["gold"] if p["kind"] == "dark" else p["function"],
        "textLink.activeForeground": p["accent"], "textBlockQuote.background": p["bg2"],
        "textBlockQuote.border": p["accent"], "textCodeBlock.background": p["bg2"],
        "textPreformat.foreground": p["string"], "sash.hoverBorder": p["accent"],

        "titleBar.activeBackground": p["bg3"], "titleBar.activeForeground": p["fg"],
        "titleBar.inactiveBackground": p["bg3"], "titleBar.inactiveForeground": p["muted"],
        "titleBar.border": p["border"],
        "commandCenter.background": p["bg2"], "commandCenter.border": p["border"],
        "commandCenter.foreground": p["fg2"], "commandCenter.activeBackground": p["hover"],

        "activityBar.background": p["bg3"], "activityBar.foreground": p["gold"] if p["kind"] == "dark" else p["accent"],
        "activityBar.inactiveForeground": p["muted"], "activityBar.activeBorder": p["accent"],
        "activityBar.border": p["border"],
        "activityBarBadge.background": p["accent"], "activityBarBadge.foreground": p["accentFg"],

        "sideBar.background": p["bg2"], "sideBar.foreground": p["fg2"], "sideBar.border": p["border"],
        "sideBarTitle.foreground": p["gold"] if p["kind"] == "dark" else p["accent"],
        "sideBarSectionHeader.background": p["bg3"], "sideBarSectionHeader.foreground": p["fg"],
        "sideBarSectionHeader.border": p["border"],

        "list.activeSelectionBackground": p["sel"], "list.activeSelectionForeground": p["fg"],
        "list.inactiveSelectionBackground": p["selInactive"], "list.hoverBackground": p["hover"],
        "list.focusOutline": p["gold"], "list.highlightForeground": p["gold"] if p["kind"] == "dark" else p["accent"],
        "list.errorForeground": p["keyword"], "list.warningForeground": p["number"],
        "tree.indentGuidesStroke": p["lineNr"],

        "editor.background": p["bg"], "editor.foreground": p["fg"],
        "editorLineNumber.foreground": p["lineNr"], "editorLineNumber.activeForeground": p["gold"] if p["kind"] == "dark" else p["accent"],
        "editorCursor.foreground": p["accent"] if p["kind"] == "light" else p["keyword"],
        "editor.selectionBackground": p["sel"], "editor.inactiveSelectionBackground": p["selInactive"],
        "editor.selectionHighlightBackground": p["selInactive"],
        "editor.wordHighlightBackground": p["selInactive"], "editor.wordHighlightStrongBackground": p["sel"],
        "editor.lineHighlightBackground": p["hl"], "editor.lineHighlightBorder": p["hl"],
        "editor.findMatchBackground": p["find"], "editor.findMatchHighlightBackground": p["findHl"],
        "editor.rangeHighlightBackground": p["findHl"],
        "editorBracketMatch.background": p["selInactive"], "editorBracketMatch.border": p["gold"],
        "editorBracketHighlight.foreground1": p["gold"], "editorBracketHighlight.foreground2": p["keyword"],
        "editorBracketHighlight.foreground3": p["string"], "editorBracketHighlight.foreground4": p["function"],
        "editorBracketHighlight.foreground5": p["type"], "editorBracketHighlight.foreground6": p["regex"],
        "editorIndentGuide.background1": p["border"], "editorIndentGuide.activeBackground1": p["lineNr"],
        "editorWhitespace.foreground": p["border"], "editorRuler.foreground": p["border"],
        "editorCodeLens.foreground": p["muted"], "editorLink.activeForeground": p["gold"],
        "editorError.foreground": a["red"], "editorWarning.foreground": a["yellow"], "editorInfo.foreground": a["blue"],
        "editorGutter.addedBackground": a["green"], "editorGutter.modifiedBackground": a["blue"],
        "editorGutter.deletedBackground": a["red"],
        "editorOverviewRuler.border": p["border"],
        "editorWidget.background": p["bg2"], "editorWidget.border": p["border"],
        "editorSuggestWidget.background": p["bg2"], "editorSuggestWidget.border": p["border"],
        "editorSuggestWidget.selectedBackground": p["sel"], "editorSuggestWidget.highlightForeground": p["gold"] if p["kind"] == "dark" else p["accent"],
        "editorHoverWidget.background": p["bg2"], "editorHoverWidget.border": p["border"],
        "peekView.border": p["accent"], "peekViewEditor.background": p["bg2"],
        "peekViewResult.background": p["bg3"], "peekViewTitle.background": p["bg3"],
        "minimap.selectionHighlight": p["sel"], "minimapSlider.background": p["lineNr"] + "33",

        "editorGroupHeader.tabsBackground": p["bg3"], "editorGroupHeader.tabsBorder": p["border"],
        "editorGroup.border": p["border"],
        "tab.activeBackground": p["bg"], "tab.activeForeground": p["fg"], "tab.activeBorderTop": p["accent"],
        "tab.inactiveBackground": p["bg3"], "tab.inactiveForeground": p["muted"], "tab.border": p["bg3"],
        "tab.hoverBackground": p["hover"], "tab.unfocusedActiveForeground": p["fg2"],
        "breadcrumb.foreground": p["muted"], "breadcrumb.focusForeground": p["fg"],
        "breadcrumb.activeSelectionForeground": p["gold"] if p["kind"] == "dark" else p["accent"],

        "statusBar.background": p["status"], "statusBar.foreground": p["statusFg"], "statusBar.border": p["statusBorder"],
        "statusBar.noFolderBackground": p["status"], "statusBar.debuggingBackground": p["gold"],
        "statusBar.debuggingForeground": p["bg3"], "statusBarItem.remoteBackground": p["accent"],
        "statusBarItem.remoteForeground": p["accentFg"], "statusBarItem.hoverBackground": "#ffffff1f",

        "panel.background": p["bg3"], "panel.border": p["border"],
        "panelTitle.activeBorder": p["accent"], "panelTitle.activeForeground": p["fg"],
        "panelTitle.inactiveForeground": p["muted"],
        "terminal.background": p["bg3"], "terminal.foreground": p["fg"], "terminalCursor.foreground": p["accent"],
        "terminal.selectionBackground": p["sel"],

        "button.background": p["accent"], "button.foreground": p["accentFg"], "button.hoverBackground": p["accentHover"],
        "button.secondaryBackground": p["hover"], "button.secondaryForeground": p["fg"],
        "badge.background": p["accent"], "badge.foreground": p["accentFg"],
        "input.background": p["bg3"] if p["kind"] == "dark" else "#ffffff", "input.border": p["border"],
        "input.foreground": p["fg"], "input.placeholderForeground": p["muted"],
        "inputOption.activeBorder": p["gold"],
        "dropdown.background": p["bg3"] if p["kind"] == "dark" else "#ffffff", "dropdown.border": p["border"],
        "checkbox.background": p["bg3"] if p["kind"] == "dark" else "#ffffff", "checkbox.border": p["border"],
        "scrollbarSlider.background": p["lineNr"] + "55", "scrollbarSlider.hoverBackground": p["lineNr"] + "88",
        "scrollbarSlider.activeBackground": p["lineNr"] + "aa",
        "progressBar.background": p["gold"] if p["kind"] == "dark" else p["accent"],
        "notifications.background": p["bg2"], "notifications.border": p["border"],
        "notificationCenterHeader.background": p["bg3"],
        "quickInput.background": p["bg2"], "quickInputList.focusBackground": p["sel"],
        "menu.background": p["bg2"], "menu.foreground": p["fg"], "menu.selectionBackground": p["sel"],
        "menu.border": p["border"],
        "gitDecoration.addedResourceForeground": a["green"], "gitDecoration.modifiedResourceForeground": p["number"],
        "gitDecoration.deletedResourceForeground": a["red"], "gitDecoration.untrackedResourceForeground": p["string"],
        "gitDecoration.ignoredResourceForeground": p["muted"],
        "diffEditor.insertedTextBackground": a["green"] + "26", "diffEditor.removedTextBackground": a["red"] + "26",
    }
    for k, v in a.items():
        c[f"terminal.ansi{k.capitalize()}"] = v
        c[f"terminal.ansiBright{k.capitalize()}"] = v
    return c


def tokens(p):
    t = lambda scope, fg=None, style=None: {"scope": scope, "settings": {k: v for k, v in (("foreground", fg), ("fontStyle", style)) if v}}
    return [
        t(["comment", "punctuation.definition.comment"], p["comment"], "italic"),
        t(["keyword", "storage", "storage.type", "storage.modifier", "keyword.control"], p["keyword"]),
        t(["string", "string.quoted", "string.template"], p["string"]),
        t(["string.regexp", "constant.character.escape"], p["regex"]),
        t(["constant.numeric", "constant.language", "constant.character", "support.constant"], p["number"]),
        t(["entity.name.function", "support.function", "meta.function-call"], p["function"]),
        t(["entity.name.type", "entity.name.class", "support.type", "support.class", "entity.other.inherited-class"], p["type"]),
        t(["variable", "variable.other", "meta.definition.variable"], p["fg"]),
        t(["variable.parameter"], p["param"]),
        t(["variable.language", "variable.language.this"], p["keyword"], "italic"),
        t(["entity.name.tag"], p["tag"]),
        t(["entity.other.attribute-name"], p["attr"]),
        t(["keyword.operator", "punctuation"], p["op"]),
        t(["meta.property-name", "support.type.property-name"], p["function"]),
        t(["entity.name.section", "markup.heading"], p["gold"] if p["kind"] == "dark" else p["accent"], "bold"),
        t(["markup.bold"], None, "bold"),
        t(["markup.italic"], None, "italic"),
        t(["markup.inline.raw", "markup.fenced_code"], p["string"]),
        t(["markup.underline.link"], p["function"]),
        t(["invalid"], p["ansi"]["red"]),
    ]


def semantic(p):
    return {
        "parameter": p["param"], "property": p["fg"], "enumMember": p["number"],
        "function": p["function"], "method": p["function"], "class": p["type"], "interface": p["type"],
        "type": p["type"], "namespace": p["type"], "*.defaultLibrary": {"italic": True},
    }


# ---------- Kontrast ----------
def lum(h):
    h = h.lstrip("#")[:6]
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    rgb = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def contrast(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


out = os.path.join(os.path.dirname(__file__), "..", "themes")
os.makedirs(out, exist_ok=True)
ok = True
for key, p in PALETTES.items():
    theme = {"name": p["label"], "type": p["kind"], "semanticHighlighting": True,
             "colors": colors(p), "tokenColors": tokens(p), "semanticTokenColors": semantic(p)}
    with open(os.path.join(out, f"weihnachten-{key}-color-theme.json"), "w", encoding="utf-8") as f:
        json.dump(theme, f, indent=2, ensure_ascii=False)

    checks = [(n, p[n], p["bg"], 4.5) for n in ("fg", "keyword", "string", "number", "function", "type", "param", "tag", "attr", "regex")]
    checks += [("comment", p["comment"], p["bg"], 3.0), ("muted (Sidebar)", p["muted"], p["bg2"], 3.0),
               ("Statusleiste", p["statusFg"], p["status"], 4.5), ("Button", p["accentFg"], p["accent"], 4.5)]
    print(f"\n{p['label']}")
    for name, fg, bg, need in checks:
        c = contrast(fg, bg)
        flag = "OK " if c >= need else "ZU TIEF"
        ok &= c >= need
        print(f"  {flag} {name:18s} {c:5.2f}:1 (min {need})")
sys.exit(0 if ok else 1)
