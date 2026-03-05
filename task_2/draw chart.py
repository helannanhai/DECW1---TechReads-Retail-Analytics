import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

def create_drawio_er_diagram(filename="books_schema.drawio"):
    # 创建根元素 <mxGraphModel> 并设置必要的命名空间
    mxGraphModel = ET.Element("mxGraphModel")
    mxGraphModel.set("dx", "1422")
    mxGraphModel.set("dy", "794")
    mxGraphModel.set("grid", "1")
    mxGraphModel.set("gridSize", "10")
    mxGraphModel.set("guides", "1")
    mxGraphModel.set("tooltips", "1")
    mxGraphModel.set("connect", "1")
    mxGraphModel.set("arrows", "1")
    mxGraphModel.set("fold", "1")
    mxGraphModel.set("page", "1")
    mxGraphModel.set("pageScale", "1")
    mxGraphModel.set("pageWidth", "1169")
    mxGraphModel.set("pageHeight", "827")
    mxGraphModel.set("background", "#ffffff")

    root = ET.Element("root")
    # 必须包含的 mxCell 单元 (0 和 1)
    cell0 = ET.SubElement(root, "mxCell", id="0")
    cell1 = ET.SubElement(root, "mxCell", id="1", parent="0")

    # 定义表的位置和样式
    table_x = 120
    table_y = 80
    cell_width = 240
    line_height = 30
    header_height = 40

    # ---- 表头单元格 ----
    cell_header = ET.SubElement(root, "mxCell",
        id="cell_header",
        value="books",
        style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=40;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;",
        vertex="1",
        parent="1")
    cell_header.set("x", str(table_x))
    cell_header.set("y", str(table_y))
    cell_header.set("width", str(cell_width))
    cell_header.set("height", str(header_height))

    # 字段列表
    fields = [
        ("id", "INT", "PRIMARY KEY, AUTO_INCREMENT"),
        ("title", "VARCHAR(255)", "NOT NULL"),
        ("author", "VARCHAR(255)", ""),
        ("year", "VARCHAR(10)", ""),
        ("rating", "DECIMAL(3,2)", ""),
        ("ratings_count", "INT", ""),
        ("reviews_count", "INT", ""),
        ("source", "VARCHAR(50)", ""),
        ("url", "VARCHAR(500)", "")
    ]

    # 记录上一个字段的 id 用于连接
    prev_field_id = None
    first_field_id = None

    # 逐个创建字段单元格
    for i, (name, dtype, extra) in enumerate(fields):
        field_id = f"field_{i}"
        value = f"{name} : {dtype}"
        if extra:
            value += f" ({extra})"
        cell_field = ET.SubElement(root, "mxCell",
            id=field_id,
            value=value,
            style="text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;whiteSpace=wrap;html=1;",
            vertex="1",
            parent="cell_header")
        cell_field.set("y", str(table_y + header_height + i * line_height))
        # 每个字段单元格相对于父级定位（y 相对父级的左上角）
        # 但 draw.io 中需要绝对坐标，这里用父级相对坐标，实际由 parent 属性处理
        # 为了简化，不设置绝对 x,y，而是依赖父级堆栈布局。但为了兼容性，我们仍设置相对坐标
        cell_field.set("relative_x", "1")   # 表示相对于父级
        cell_field.set("relative_y", "1")
        # 实际在 mxCell 中，使用 geometry 子元素定义相对位置
        geo = ET.SubElement(cell_field, "mxGeometry")
        geo.set("y", str(i * line_height))
        geo.set("width", str(cell_width))
        geo.set("height", str(line_height))
        geo.set("as", "geometry")

        if i == 0:
            first_field_id = field_id
        else:
            # 可以添加连线，但不是必须的，ER 图中通常不需要字段之间的线
            pass

    # 设置表的总高度
    cell_header.set("height", str(header_height + len(fields) * line_height))

    # 构建完整的 XML 树
    root.append(cell0)
    root.append(cell1)
    mxGraphModel.append(root)

    # 生成格式化的 XML 字符串
    rough_string = ET.tostring(mxGraphModel, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    # 写入文件
    with open(filename, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"draw.io diagram saved to {filename}")

if __name__ == "__main__":
    create_drawio_er_diagram()