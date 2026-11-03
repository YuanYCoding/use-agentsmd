"""Generate original, editable SVG illustrations for the project documentation."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "images"
OUT.mkdir(parents=True, exist_ok=True)
FG, MUTED, GREEN, BLUE, PURPLE, AMBER = "#edf3f8", "#a9b9cc", "#b5f0a2", "#87d9fa", "#bba9ff", "#f0cb8d"


class Canvas:
    def __init__(self, title, height=820, width=1440):
        self.width, self.height = width, height
        self.items = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#101d31"/><stop offset="1" stop-color="#08111e"/></linearGradient>
<pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M 48 0 L 0 0 0 48" fill="none" stroke="#223449" stroke-width="0.6" opacity="0.45"/></pattern>
<linearGradient id="line"><stop stop-color="#b5f0a2"/><stop offset="1" stop-color="#87d9fa"/></linearGradient></defs>
<rect width="{width}" height="{height}" rx="24" fill="url(#bg)"/><rect width="{width}" height="{height}" rx="24" fill="url(#grid)"/>
<style>text{{font-family:Inter,'Segoe UI','Microsoft YaHei','Noto Sans CJK SC',sans-serif}} .mono{{font-family:'Cascadia Code',Consolas,'Microsoft YaHei',monospace}}</style>''']

    def rect(self, x, y, w, h, fill="#15243a", stroke="#31435c", radius=18):
        self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>')

    def text(self, x, y, value, size=26, color=FG, weight=400, cls="", anchor="start"):
        self.items.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" class="{cls}" text-anchor="{anchor}">{escape(value)}</text>')

    def line(self, x1, y1, x2, y2, color="#607a97", width=2):
        self.items.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}"/>')

    def arrow(self, x1, y1, x2, y2, color=BLUE):
        self.line(x1, y1, x2, y2, color, 3)
        if x1 == x2:
            self.items.append(f'<path d="M{x2-7} {y2-10} L{x2} {y2} L{x2+7} {y2-10}" fill="none" stroke="{color}" stroke-width="3"/>')
        else:
            self.items.append(f'<path d="M{x2-10} {y2-7} L{x2} {y2} L{x2-10} {y2+7}" fill="none" stroke="{color}" stroke-width="3"/>')

    def pill(self, x, y, w, label, color=GREEN):
        self.rect(x, y, w, 44, "#182a3d", "#395267", 22)
        self.text(x+w/2, y+29, label, 19, color, 600, anchor="middle")

    def header(self, eyebrow, title, subtitle):
        self.text(64, 57, eyebrow, 18, GREEN, 600)
        self.text(64, 119, title, 44, FG, 700)
        self.text(64, 164, subtitle, 23, MUTED)

    def footer(self, note="use-agentsmd  /  Project guidance, kept current."):
        self.text(64, self.height-34, note, 17, "#8c9eb5")

    def save(self, name):
        (OUT / f"{name}.svg").write_text("\n".join(self.items)+"\n</svg>\n", encoding="utf-8")


def hero():
    c=Canvas("use-agentsmd — 让项目规则跟上 Vibe coding 的变化", 690)
    c.text(72, 88, "AGENT SKILL  /  VIBE CODING", 19, GREEN, 600)
    c.text(68, 226, "use-agentsmd", 89, FG, 750)
    c.text(72, 305, "让项目规则，跟上代码的变化。", 38, FG, 600)
    c.text(74, 365, "开工前创建 · 跑通后校准 · 长期约定变化时更新", 24, MUTED)
    c.text(74, 409, "从原型到维护，给下一位 AI 一份准确的项目说明。", 24, MUTED)
    c.pill(74, 499, 184, "阶段判断", GREEN)
    c.pill(276, 499, 184, "项目证据", BLUE)
    c.pill(478, 499, 220, "最小必要更新", PURPLE)
    c.rect(954, 125, 394, 412, "#0b1626", "#415976", 22)
    c.rect(979, 101, 344, 58, "#1c3147", "#496078", 16)
    c.text(1010, 140, "AGENTS.md", 31, GREEN, 650, "mono")
    for i,(label,color,bars) in enumerate([("Project context",BLUE,[236,185]),("Commands & checks",PURPLE,[254,162]),("Working conventions",AMBER,[230,192])]):
        y=216+i*104
        c.text(987,y,label,22,color,600)
        for j,w in enumerate(bars): c.rect(987,y+19+j*18,w,6,"#30455f","none",3)
    c.line(72,586,1348,586,"#30455f")
    c.text(74,630,"Adopts the AGENTS.md convention · Independent community project",19,MUTED)
    c.save("hero")


def lifecycle():
    c=Canvas("六个阶段，六种 AGENTS.md 维护重点", 850)
    c.header("01 / LIFECYCLE", "项目在变化，记录重点也随之变化", "先判断实际阶段，再选择有证据、会持续适用的内容。")
    cards=[("01","开工","START",GREEN,["项目目标与首期范围","已确认的技术选择","工作边界"]),
           ("02","搭建","BOOTSTRAP",BLUE,["实际目录与包管理器","安装、启动与检查入口","必要环境前提"]),
           ("03","首个可用版本","FIRST WORKING VERSION",PURPLE,["代码组织与公共组件","接口和数据约定","核心流程验证入口"]),
           ("04","持续迭代","ITERATE",GREEN,["新的长期开发约定","模块职责与复用入口","相关检查要求"]),
           ("05","重构","REFACTOR",BLUE,["迁移目标与实际状态","新命令、新目录与契约","清理已失效的说明"]),
           ("06","上线与维护","OPERATE",AMBER,["验证与部署入口","运维和配置文档","适用的操作要求"])]
    for i,(num,title,en,col,lines) in enumerate(cards):
        x=64+(i%3)*444; y=209+(i//3)*278
        c.rect(x,y,424,252)
        c.text(x+24,y+42,num,22,col,700,"mono")
        c.text(x+76,y+43,title,29,FG,650)
        c.text(x+25,y+75,en,14,MUTED,600)
        for j,t in enumerate(lines):
            c.text(x+25,y+123+j*44,"·",26,col,600)
            c.text(x+45,y+123+j*44,t,23,FG)
    c.footer("阶段是维护方法，非官方强制模型；不同模块可以处于不同阶段。")
    c.save("lifecycle")


def workflow():
    c=Canvas("从读取项目到创建、更新或保持不变的工作流程", 950)
    c.header("02 / WORKFLOW", "创建、更新，或保持不变", "文件是否存在决定处理分支；项目证据决定写入内容。")
    for i,(title,sub) in enumerate([("定位项目","确认根目录与范围"),("读取证据","文档、脚本与现有规则"),("判断阶段","成熟度 + 当前任务")]):
        x=142+i*392
        c.rect(x,211,350,105)
        c.text(x+175,252,title,29,FG,650,anchor="middle")
        c.text(x+175,287,sub,20,MUTED,anchor="middle")
        if i<2: c.arrow(x+355,263,x+384,263)
    c.arrow(1100,316,1100,346)
    c.line(1100,346,720,346,BLUE,3)
    c.arrow(720,346,720,370)
    c.rect(485,370,470,78,"#193443","#5e8a93",18)
    c.text(720,418,"根 AGENTS.md 是否存在？",28,GREEN,650,anchor="middle")
    c.line(485,409,300,409,BLUE,3); c.arrow(300,409,300,513)
    c.text(334,453,"不存在",21,BLUE)
    c.line(955,409,1110,409,BLUE,3); c.arrow(1110,409,1110,513)
    c.text(1000,453,"已存在",21,BLUE)
    c.rect(100,513,402,112,"#183529","#4b7659")
    c.text(301,555,"按当前阶段创建",30,GREEN,650,anchor="middle")
    c.text(301,591,"成熟项目也可以首次补建",21,MUTED,anchor="middle")
    c.rect(900,513,420,112)
    c.text(1110,555,"是否有有效的长期变化？",26,FG,650,anchor="middle")
    c.text(1110,591,"已有依据 · 持续适用 · 有助工作",19,MUTED,anchor="middle")
    c.line(1000,625,1000,651,BLUE,3); c.line(1000,651,825,651,BLUE,3); c.arrow(825,651,825,691)
    c.line(1225,625,1225,651,BLUE,3); c.arrow(1225,651,1225,691)
    c.text(858,681,"有",20,BLUE); c.text(1252,681,"无",20,AMBER)
    c.rect(654,691,342,90,"#202b45","#6c6295")
    c.text(825,729,"最小必要更新",27,PURPLE,650,anchor="middle")
    c.text(825,760,"保留 · 补充 · 替换 · 清理",19,MUTED,anchor="middle")
    c.rect(1044,691,336,90,"#302d25","#796b4c")
    c.text(1212,729,"保持不变",27,AMBER,650,anchor="middle")
    c.text(1212,760,"不重复追加，不制造改动",19,MUTED,anchor="middle")
    c.arrow(301,625,301,811)
    c.rect(100,811,1280,68,"#152d37","#426572")
    c.text(740,854,"核对实际文件与差异，说明阶段依据、变化和验证范围",25,FG,600,anchor="middle")
    c.line(825,781,825,811,BLUE,3); c.line(1212,781,1212,811,BLUE,3)
    c.footer()
    c.save("workflow")


def before_after():
    c=Canvas("重构后更新 AGENTS.md 的说明性示例", 790)
    c.header("03 / EXAMPLE UPDATE", "把过时说明，更新为准确约定", "示例：项目已切换包管理器与目录，接口约定继续有效。")
    c.rect(64,218,610,429,"#251f2c","#5c4658")
    c.rect(766,218,610,429,"#162c2a","#496d59")
    c.text(94,264,"BEFORE",22,"#edb0af",700)
    c.text(796,264,"AFTER",22,GREEN,700)
    left=[("# Commands",MUTED),("npm run dev",FG),("npm test",FG),("",FG),("# Code layout",MUTED),("src/logic/",FG),("",FG),("# API contract",MUTED),("{ data, error }",FG)]
    right=[("# Commands",MUTED),("pnpm dev",GREEN),("pnpm check",GREEN),("仅检查入口文件语法",MUTED),("# Code layout",MUTED),("src/services/",GREEN),("",FG),("# API contract",MUTED),("{ data, error }",FG)]
    for rows,x in [(left,94),(right,796)]:
        for i,(value,col) in enumerate(rows): c.text(x,310+i*35,value,23,col,400,"mono")
    c.arrow(690,424,748,424,GREEN)
    c.pill(64,683,270,"核实后的命令",GREEN)
    c.pill(358,683,270,"明确检查范围",BLUE)
    c.pill(652,683,270,"保留有效约定",PURPLE)
    c.pill(946,683,430,"按目标项目生成，示例不直接套用",AMBER)
    c.footer()
    c.save("before-after")


def content_filter():
    c=Canvas("区分长期项目约定与一次性任务信息", 800)
    c.header("04 / CONTENT FILTER", "留下约定，让下一位 AI 少走弯路", "已经确认 + 持续适用 + 有助后续工作，才值得进入项目说明。")
    c.rect(64,218,634,420,"#152f2b","#466f5b")
    c.rect(742,218,634,420,"#28283a","#5f577a")
    c.text(96,272,"写入 AGENTS.md",30,GREEN,650)
    c.text(774,272,"留在任务或交付记录",30,PURPLE,650)
    items=[("统一使用现有请求模块","这次把按钮文字改成“立即保存”"),
           ("实际有效的命令和执行目录","今天做到哪一步、下一步做什么"),
           ("已确认的接口与复用约定","尚未采用的实验方案"),
           ("项目特有的操作条件和注意事项","未证实的故障猜测与临时绕过")]
    for i,(a,b) in enumerate(items):
        y=340+i*75
        c.text(97,y,"+",24,GREEN,700); c.text(127,y,a,24,FG)
        c.text(775,y,"·",28,PURPLE,700); c.text(805,y,b,23,FG)
    c.rect(64,679,1312,63,"#142236","#3c506b",14)
    c.text(720,719,"局部纠正保留局部范围；过时规则及时替换；没有变化就保持不变。",25,FG,500,anchor="middle")
    c.footer()
    c.save("content-filter")


if __name__ == "__main__":
    for build in (hero,lifecycle,workflow,before_after,content_filter): build()
    print(f"Generated 5 SVG illustrations in {OUT}")
