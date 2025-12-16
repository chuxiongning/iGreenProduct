"""
Generate Database Schema Documentation in Word Format
生成Word格式的数据库表结构文档
"""
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from datetime import datetime

# Database schema information extracted from SQLAlchemy models
TABLES = {
    "users": {
        "name_zh": "用户表",
        "description": "存储系统用户信息，包括管理员、工程师和经理",
        "fields": [
            {"name": "id", "type": "VARCHAR(36)", "null": "NO", "key": "PRI", "default": None, "extra": "UUID", "comment": "主键，UUID格式"},
            {"name": "name", "type": "VARCHAR(255)", "null": "NO", "key": "", "default": None, "extra": "", "comment": "用户全名"},
            {"name": "username", "type": "VARCHAR(100)", "null": "NO", "key": "UNI", "default": None, "extra": "", "comment": "用户名（唯一）"},
            {"name": "email", "type": "VARCHAR(255)", "null": "NO", "key": "UNI", "default": None, "extra": "", "comment": "邮箱地址（唯一）"},
            {"name": "hashed_password", "type": "VARCHAR(255)", "null": "NO", "key": "", "default": None, "extra": "", "comment": "加密后的密码"},
            {"name": "role", "type": "ENUM", "null": "NO", "key": "", "default": "engineer", "extra": "admin, engineer, manager", "comment": "用户角色"},
            {"name": "status", "type": "ENUM", "null": "NO", "key": "", "default": "active", "extra": "active, inactive", "comment": "用户状态"},
            {"name": "group_id", "type": "VARCHAR(36)", "null": "YES", "key": "FK", "default": None, "extra": "FK→groups.id, ON DELETE SET NULL", "comment": "所属分组ID"},
            {"name": "created_at", "type": "DATETIME", "null": "NO", "key": "", "default": "CURRENT_TIMESTAMP", "extra": "", "comment": "创建时间"},
            {"name": "updated_at", "type": "DATETIME", "null": "NO", "key": "", "default": "CURRENT_TIMESTAMP ON UPDATE", "extra": "", "comment": "更新时间"},
        ],
        "indexes": ["PRIMARY KEY (id)", "UNIQUE INDEX (username)", "UNIQUE INDEX (email)", "INDEX (group_id)"]
    },
    "groups": {
        "name_zh": "分组表",
        "description": "存储用户分组信息，用于组织和管理用户",
        "fields": [
            {"name": "id", "type": "VARCHAR(36)", "null": "NO", "key": "PRI", "default": None, "extra": "UUID", "comment": "主键，UUID格式"},
            {"name": "name", "type": "VARCHAR(255)", "null": "NO", "key": "UNI", "default": None, "extra": "", "comment": "分组名称（唯一）"},
            {"name": "description", "type": "VARCHAR(500)", "null": "YES", "key": "", "default": None, "extra": "", "comment": "分组描述"},
            {"name": "tags", "type": "JSON", "null": "YES", "key": "", "default": "[]", "extra": "", "comment": "标签列表"},
            {"name": "status", "type": "ENUM", "null": "NO", "key": "", "default": "active", "extra": "active, inactive", "comment": "分组状态"},
            {"name": "created_at", "type": "DATETIME", "null": "NO", "key": "", "default": "CURRENT_TIMESTAMP", "extra": "", "comment": "创建时间"},
            {"name": "updated_at", "type": "DATETIME", "null": "NO", "key": "", "default": "CURRENT_TIMESTAMP ON UPDATE", "extra": "", "comment": "更新时间"},
        ],
        "indexes": ["PRIMARY KEY (id)", "UNIQUE INDEX (name)"]
    },
    "sites": {
        "name_zh": "站点表",
        "description": "存储EV充电站点信息，包括地址和状态",
        "fields": [
            {"name": "id", "type": "VARCHAR(36)", "null": "NO", "key": "PRI", "default": None, "extra": "UUID", "comment": "主键，UUID格式"},
            {"name": "name", "type": "VARCHAR(255)", "null": "NO", "key": "UNI", "default": None, "extra": "", "comment": "站点名称（唯一）"},
            {"name": "address", "type": "VARCHAR(500)", "null": "NO", "key": "", "default": None, "extra": "", "comment": "站点地址"},
            {"name": "level", "type": "VARCHAR(50)", "null": "NO", "key": "", "default": "normal", "extra": "", "comment": "站点级别（normal, vip等）"},
            {"name": "status", "type": "ENUM", "null": "NO", "key": "", "default": "online", "extra": "online, offline, underConstruction", "comment": "站点状态"},
            {"name": "created_at", "type": "DATETIME", "null": "NO", "key": "", "default": "CURRENT_TIMESTAMP", "extra": "", "comment": "创建时间"},
            {"name": "updated_at", "type": "DATETIME", "null": "NO", "key": "", "default": "CURRENT_TIMESTAMP ON UPDATE", "extra": "", "comment": "更新时间"},
        ],
        "indexes": ["PRIMARY KEY (id)", "UNIQUE INDEX (name)"]
    },
    "site_level_configs": {
        "name_zh": "站点级别配置表",
        "description": "存储不同站点级别的配置信息，如SLA倍数",
        "fields": [
            {"name": "id", "type": "VARCHAR(36)", "null": "NO", "key": "PRI", "default": None, "extra": "UUID", "comment": "主键，UUID格式"},
            {"name": "name", "type": "VARCHAR(255)", "null": "NO", "key": "UNI", "default": None, "extra": "", "comment": "级别名称（唯一）"},
            {"name": "description", "type": "TEXT", "null": "YES", "key": "", "default": None, "extra": "", "comment": "级别描述"},
            {"name": "sla_multiplier", "type": "FLOAT", "null": "NO", "key": "", "default": "1.0", "extra": "", "comment": "SLA时间倍数"},
        ],
        "indexes": ["PRIMARY KEY (id)", "UNIQUE INDEX (name)"]
    },
    "tickets": {
        "name_zh": "工单表",
        "description": "存储维护工单信息，是系统的核心业务表",
        "fields": [
            {"name": "id", "type": "VARCHAR(36)", "null": "NO", "key": "PRI", "default": None, "extra": "UUID", "comment": "主键，UUID格式"},
            {"name": "title", "type": "VARCHAR(500)", "null": "NO", "key": "", "default": None, "extra": "", "comment": "工单标题"},
            {"name": "description", "type": "TEXT", "null": "YES", "key": "", "default": None, "extra": "", "comment": "工单详细描述"},
            {"name": "type", "type": "ENUM", "null": "NO", "key": "", "default": None, "extra": "planned, preventive, corrective, problem", "comment": "工单类型"},
            {"name": "status", "type": "ENUM", "null": "NO", "key": "", "default": "open", "extra": "open, accepted, inProgress, closed, onHold, cancelled, submitted", "comment": "工单状态"},
            {"name": "priority", "type": "ENUM", "null": "YES", "key": "", "default": None, "extra": "P1, P2, P3, P4", "comment": "优先级"},
            {"name": "site", "type": "VARCHAR(255)", "null": "YES", "key": "", "default": None, "extra": "", "comment": "站点名称"},
            {"name": "template_id", "type": "VARCHAR(36)", "null": "NO", "key": "FK", "default": None, "extra": "FK→templates.id, ON DELETE RESTRICT", "comment": "关联模板ID"},
            {"name": "assigned_to", "type": "VARCHAR(36)", "null": "NO", "key": "FK", "default": None, "extra": "FK→users.id, ON DELETE RESTRICT", "comment": "分配的工程师ID"},
            {"name": "created_by", "type": "VARCHAR(36)", "null": "NO", "key": "FK", "default": None, "extra": "FK→users.id, ON DELETE RESTRICT", "comment": "创建者ID"},
            {"name": "completed_steps", "type": "JSON", "null": "YES", "key": "", "default": "[]", "extra": "", "comment": "已完成步骤ID列表"},
            {"name": "step_data", "type": "JSON", "null": "YES", "key": "", "default": "{}", "extra": "", "comment": "步骤数据（字段值）"},
            {"name": "accepted", "type": "BOOLEAN", "null": "YES", "key": "", "default": None, "extra": "", "comment": "是否接受工单"},
            {"name": "accepted_at", "type": "DATETIME", "null": "YES", "key": "", "default": None, "extra": "", "comment": "接受时间"},
            {"name": "departure_at", "type": "DATETIME", "null": "YES", "key": "", "default": None, "extra": "", "comment": "出发时间"},
            {"name": "departure_photo", "type": "VARCHAR(500)", "null": "YES", "key": "", "default": None, "extra": "", "comment": "出发照片URL"},
            {"name": "arrival_at", "type": "DATETIME", "null": "YES", "key": "", "default": None, "extra": "", "comment": "到达现场时间"},
            {"name": "arrival_photo", "type": "VARCHAR(500)", "null": "YES", "key": "", "default": None, "extra": "", "comment": "到达现场照片URL"},
            {"name": "completion_photo", "type": "VARCHAR(500)", "null": "YES", "key": "", "default": None, "extra": "", "comment": "完成工作照片URL"},
            {"name": "cause", "type": "TEXT", "null": "YES", "key": "", "default": None, "extra": "", "comment": "问题原因"},
            {"name": "solution", "type": "TEXT", "null": "YES", "key": "", "default": None, "extra": "", "comment": "解决方案"},
            {"name": "related_ticket_ids", "type": "JSON", "null": "YES", "key": "", "default": "[]", "extra": "", "comment": "关联工单ID列表"},
            {"name": "created_at", "type": "DATETIME", "null": "NO", "key": "", "default": "CURRENT_TIMESTAMP", "extra": "", "comment": "创建时间"},
            {"name": "updated_at", "type": "DATETIME", "null": "NO", "key": "", "default": "CURRENT_TIMESTAMP ON UPDATE", "extra": "", "comment": "更新时间"},
            {"name": "due_date", "type": "DATETIME", "null": "NO", "key": "", "default": None, "extra": "", "comment": "截止时间"},
        ],
        "indexes": ["PRIMARY KEY (id)", "INDEX (template_id)", "INDEX (assigned_to)", "INDEX (created_by)", "INDEX (status)"]
    },
    "ticket_comments": {
        "name_zh": "工单评论表",
        "description": "存储工单的评论和操作记录",
        "fields": [
            {"name": "id", "type": "VARCHAR(36)", "null": "NO", "key": "PRI", "default": None, "extra": "UUID", "comment": "主键，UUID格式"},
            {"name": "comment", "type": "TEXT", "null": "NO", "key": "", "default": None, "extra": "", "comment": "评论内容"},
            {"name": "type", "type": "ENUM", "null": "NO", "key": "", "default": "general", "extra": "general, accept, decline, cancel", "comment": "评论类型"},
            {"name": "ticket_id", "type": "VARCHAR(36)", "null": "NO", "key": "FK", "default": None, "extra": "FK→tickets.id, ON DELETE CASCADE", "comment": "关联工单ID"},
            {"name": "user_id", "type": "VARCHAR(36)", "null": "NO", "key": "FK", "default": None, "extra": "FK→users.id, ON DELETE RESTRICT", "comment": "评论用户ID"},
            {"name": "created_at", "type": "DATETIME", "null": "NO", "key": "", "default": "CURRENT_TIMESTAMP", "extra": "", "comment": "创建时间"},
        ],
        "indexes": ["PRIMARY KEY (id)", "INDEX (ticket_id)", "INDEX (user_id)"]
    },
    "templates": {
        "name_zh": "模板表",
        "description": "存储维护工作流程模板",
        "fields": [
            {"name": "id", "type": "VARCHAR(36)", "null": "NO", "key": "PRI", "default": None, "extra": "UUID", "comment": "主键，UUID格式"},
            {"name": "name", "type": "VARCHAR(255)", "null": "NO", "key": "UNI", "default": None, "extra": "", "comment": "模板名称（唯一）"},
            {"name": "description", "type": "TEXT", "null": "YES", "key": "", "default": None, "extra": "", "comment": "模板描述"},
            {"name": "created_at", "type": "DATETIME", "null": "NO", "key": "", "default": "CURRENT_TIMESTAMP", "extra": "", "comment": "创建时间"},
            {"name": "updated_at", "type": "DATETIME", "null": "NO", "key": "", "default": "CURRENT_TIMESTAMP ON UPDATE", "extra": "", "comment": "更新时间"},
        ],
        "indexes": ["PRIMARY KEY (id)", "UNIQUE INDEX (name)"]
    },
    "template_steps": {
        "name_zh": "模板步骤表",
        "description": "存储模板的工作步骤",
        "fields": [
            {"name": "id", "type": "VARCHAR(36)", "null": "NO", "key": "PRI", "default": None, "extra": "UUID", "comment": "主键，UUID格式"},
            {"name": "name", "type": "VARCHAR(255)", "null": "NO", "key": "", "default": None, "extra": "", "comment": "步骤名称"},
            {"name": "description", "type": "TEXT", "null": "YES", "key": "", "default": None, "extra": "", "comment": "步骤描述"},
            {"name": "order", "type": "INTEGER", "null": "NO", "key": "", "default": None, "extra": "", "comment": "步骤顺序"},
            {"name": "template_id", "type": "VARCHAR(36)", "null": "NO", "key": "FK", "default": None, "extra": "FK→templates.id, ON DELETE CASCADE", "comment": "所属模板ID"},
        ],
        "indexes": ["PRIMARY KEY (id)", "INDEX (template_id)"]
    },
    "template_fields": {
        "name_zh": "模板字段表",
        "description": "存储步骤中的数据字段定义",
        "fields": [
            {"name": "id", "type": "VARCHAR(36)", "null": "NO", "key": "PRI", "default": None, "extra": "UUID", "comment": "主键，UUID格式"},
            {"name": "name", "type": "VARCHAR(255)", "null": "NO", "key": "", "default": None, "extra": "", "comment": "字段名称"},
            {"name": "type", "type": "ENUM", "null": "NO", "key": "", "default": None, "extra": "text, number, date, location, photo, signature, faceRecognition", "comment": "字段类型"},
            {"name": "required", "type": "BOOLEAN", "null": "NO", "key": "", "default": "FALSE", "extra": "", "comment": "是否必填"},
            {"name": "step_id", "type": "VARCHAR(36)", "null": "NO", "key": "FK", "default": None, "extra": "FK→template_steps.id, ON DELETE CASCADE", "comment": "所属步骤ID"},
        ],
        "indexes": ["PRIMARY KEY (id)", "INDEX (step_id)"]
    },
    "sla_configs": {
        "name_zh": "SLA配置表",
        "description": "存储不同优先级的响应时间和解决时间配置",
        "fields": [
            {"name": "id", "type": "VARCHAR(36)", "null": "NO", "key": "PRI", "default": None, "extra": "UUID", "comment": "主键，UUID格式"},
            {"name": "priority", "type": "ENUM", "null": "NO", "key": "UNI", "default": None, "extra": "P1, P2, P3, P4", "comment": "优先级（唯一）"},
            {"name": "response_time", "type": "INTEGER", "null": "NO", "key": "", "default": None, "extra": "", "comment": "响应时间（分钟）"},
            {"name": "resolution_time", "type": "INTEGER", "null": "NO", "key": "", "default": None, "extra": "", "comment": "解决时间（分钟）"},
        ],
        "indexes": ["PRIMARY KEY (id)", "UNIQUE INDEX (priority)"]
    },
    "problem_types": {
        "name_zh": "问题类型表",
        "description": "存储可用的问题类型",
        "fields": [
            {"name": "id", "type": "VARCHAR(36)", "null": "NO", "key": "PRI", "default": None, "extra": "UUID", "comment": "主键，UUID格式"},
            {"name": "name", "type": "VARCHAR(255)", "null": "NO", "key": "UNI", "default": None, "extra": "", "comment": "问题类型名称（唯一）"},
            {"name": "description", "type": "TEXT", "null": "YES", "key": "", "default": None, "extra": "", "comment": "问题类型描述"},
        ],
        "indexes": ["PRIMARY KEY (id)", "UNIQUE INDEX (name)"]
    },
    "files": {
        "name_zh": "文件表",
        "description": "存储上传的文件信息（照片、签名等）",
        "fields": [
            {"name": "id", "type": "VARCHAR(36)", "null": "NO", "key": "PRI", "default": None, "extra": "UUID", "comment": "主键，UUID格式"},
            {"name": "name", "type": "VARCHAR(500)", "null": "NO", "key": "", "default": None, "extra": "", "comment": "文件名"},
            {"name": "url", "type": "VARCHAR(1000)", "null": "NO", "key": "", "default": None, "extra": "", "comment": "文件URL或路径"},
            {"name": "type", "type": "VARCHAR(100)", "null": "NO", "key": "", "default": None, "extra": "", "comment": "文件MIME类型"},
            {"name": "size", "type": "INTEGER", "null": "NO", "key": "", "default": None, "extra": "", "comment": "文件大小（字节）"},
            {"name": "field_type", "type": "VARCHAR(50)", "null": "YES", "key": "", "default": None, "extra": "", "comment": "字段类型（photo, signature等）"},
            {"name": "created_at", "type": "DATETIME", "null": "NO", "key": "", "default": "CURRENT_TIMESTAMP", "extra": "", "comment": "上传时间"},
        ],
        "indexes": ["PRIMARY KEY (id)"]
    },
}

# Enum definitions
ENUMS = {
    "UserRole": {
        "description": "用户角色",
        "values": ["admin (管理员)", "engineer (工程师)", "manager (经理)"]
    },
    "UserStatus": {
        "description": "用户状态",
        "values": ["active (激活)", "inactive (未激活)"]
    },
    "GroupStatus": {
        "description": "分组状态",
        "values": ["active (激活)", "inactive (未激活)"]
    },
    "SiteStatus": {
        "description": "站点状态",
        "values": ["online (在线)", "offline (离线)", "underConstruction (建设中)"]
    },
    "TicketStatus": {
        "description": "工单状态",
        "values": ["open (新建)", "accepted (已接受)", "inProgress (进行中)", "closed (已关闭)", "onHold (暂停)", "cancelled (已取消)", "submitted (已提交)"]
    },
    "TicketType": {
        "description": "工单类型",
        "values": ["planned (计划)", "preventive (预防性)", "corrective (纠正性)", "problem (问题)"]
    },
    "Priority": {
        "description": "优先级",
        "values": ["P1 (最高)", "P2 (高)", "P3 (中)", "P4 (低)"]
    },
    "CommentType": {
        "description": "评论类型",
        "values": ["general (常规)", "accept (接受)", "decline (拒绝)", "cancel (取消)"]
    },
    "FieldType": {
        "description": "字段类型",
        "values": ["text (文本)", "number (数字)", "date (日期)", "location (位置)", "photo (照片)", "signature (签名)", "faceRecognition (人脸识别)"]
    },
}


def set_cell_border(cell, **kwargs):
    """
    Set cell borders
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()

    for edge in ('top', 'left', 'bottom', 'right'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'tc{}'.format(edge.capitalize())
            element = OxmlElement('w:{}'.format(tag))
            for key, value in edge_data.items():
                element.set(qn('w:{}'.format(key)), str(value))
            tcPr.append(element)


def add_table_header(table, headers):
    """Add formatted header row to table"""
    header_row = table.rows[0]
    header_row.height = Inches(0.4)

    for idx, header_text in enumerate(headers):
        cell = header_row.cells[idx]
        cell.text = header_text

        # Format header cell
        paragraph = cell.paragraphs[0]
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = paragraph.runs[0]
        run.font.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(255, 255, 255)

        # Set background color
        shading = OxmlElement('w:shd')
        shading.set(qn('w:fill'), '0ea5e9')  # Blue color
        cell._element.get_or_add_tcPr().append(shading)

        # Set vertical alignment
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def create_database_documentation():
    """Create comprehensive database documentation in Word format"""

    # Create document
    doc = Document()

    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Microsoft YaHei'
    font.size = Pt(10.5)

    # Title Page
    title = doc.add_heading('iGreen 充电站维护工单系统', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    subtitle = doc.add_heading('数据库表结构文档', level=1)
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Add metadata
    doc.add_paragraph()
    metadata = doc.add_paragraph()
    metadata.alignment = WD_ALIGN_PARAGRAPH.CENTER
    metadata.add_run(f'生成日期: {datetime.now().strftime("%Y年%m月%d日")}\n')
    metadata.add_run('版本: 1.0\n')
    metadata.add_run('技术栈: FastAPI + SQLAlchemy + MySQL/SQLite')

    # Page break
    doc.add_page_break()

    # Table of Contents
    doc.add_heading('目录', level=1)
    toc_para = doc.add_paragraph()
    toc_para.add_run('1. 数据库概述\n')
    toc_para.add_run('2. 表结构详细说明\n')
    for idx, (table_name, table_info) in enumerate(TABLES.items(), 1):
        toc_para.add_run(f'   2.{idx} {table_name} - {table_info["name_zh"]}\n')
    toc_para.add_run('3. 枚举类型定义\n')
    toc_para.add_run('4. 外键关系\n')
    toc_para.add_run('5. 索引说明\n')

    # Page break
    doc.add_page_break()

    # Overview Section
    doc.add_heading('1. 数据库概述', level=1)

    overview_text = f"""
iGreen充电站维护工单系统数据库包含 {len(TABLES)} 个核心表，用于管理EV充电站的维护工作流程。

数据库设计特点：
• 使用UUID作为主键，确保分布式环境下的唯一性
• 采用枚举类型约束数据一致性
• JSON字段支持灵活的扩展数据存储
• 完善的外键关系和级联删除策略
• 自动时间戳管理（created_at, updated_at）

总字段数：{sum(len(table['fields']) for table in TABLES.values())} 个
总索引数：{sum(len(table['indexes']) for table in TABLES.values())} 个
"""
    doc.add_paragraph(overview_text.strip())

    # Statistics table
    doc.add_heading('数据库统计信息', level=2)
    stats_table = doc.add_table(rows=len(TABLES) + 1, cols=4)
    stats_table.style = 'Light Grid Accent 1'

    add_table_header(stats_table, ['表名', '中文名', '字段数', '索引数'])

    for idx, (table_name, table_info) in enumerate(TABLES.items(), 1):
        row = stats_table.rows[idx]
        row.cells[0].text = table_name
        row.cells[1].text = table_info['name_zh']
        row.cells[2].text = str(len(table_info['fields']))
        row.cells[3].text = str(len(table_info['indexes']))

        # Center align
        for cell in row.cells:
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Page break
    doc.add_page_break()

    # Detailed Table Descriptions
    doc.add_heading('2. 表结构详细说明', level=1)

    for table_idx, (table_name, table_info) in enumerate(TABLES.items(), 1):
        # Table heading
        doc.add_heading(f'2.{table_idx} {table_name} - {table_info["name_zh"]}', level=2)

        # Table description
        desc_para = doc.add_paragraph()
        desc_para.add_run('描述: ').bold = True
        desc_para.add_run(table_info['description'])

        # Field count
        field_count_para = doc.add_paragraph()
        field_count_para.add_run('字段数: ').bold = True
        field_count_para.add_run(str(len(table_info['fields'])))

        # Fields table
        doc.add_paragraph()
        fields_table = doc.add_table(rows=len(table_info['fields']) + 1, cols=7)
        fields_table.style = 'Light Grid Accent 1'

        add_table_header(fields_table, ['字段名', '类型', '允许空', '键', '默认值', '额外信息', '说明'])

        for field_idx, field in enumerate(table_info['fields'], 1):
            row = fields_table.rows[field_idx]
            row.cells[0].text = field['name']
            row.cells[1].text = field['type']
            row.cells[2].text = field['null']
            row.cells[3].text = field['key']
            row.cells[4].text = str(field['default']) if field['default'] else ''
            row.cells[5].text = field['extra']
            row.cells[6].text = field['comment']

            # Format cells
            for cell in row.cells[:4]:
                cell.paragraphs[0].runs[0].font.size = Pt(9)

        # Indexes
        if table_info['indexes']:
            doc.add_paragraph()
            index_para = doc.add_paragraph()
            index_para.add_run('索引: ').bold = True
            index_text = '\n'.join(f'  • {idx}' for idx in table_info['indexes'])
            index_para.add_run('\n' + index_text)

        # Add spacing
        doc.add_paragraph()

    # Page break
    doc.add_page_break()

    # Enum Definitions
    doc.add_heading('3. 枚举类型定义', level=1)

    enum_para = doc.add_paragraph(
        '系统使用枚举类型来约束特定字段的取值范围，确保数据一致性和完整性。'
    )
    doc.add_paragraph()

    for enum_name, enum_info in ENUMS.items():
        enum_heading = doc.add_heading(enum_name, level=2)

        desc_para = doc.add_paragraph()
        desc_para.add_run('说明: ').bold = True
        desc_para.add_run(enum_info['description'])

        values_para = doc.add_paragraph()
        values_para.add_run('可选值:\n').bold = True
        for value in enum_info['values']:
            values_para.add_run(f'  • {value}\n')

        doc.add_paragraph()

    # Page break
    doc.add_page_break()

    # Foreign Key Relationships
    doc.add_heading('4. 外键关系', level=1)

    fk_intro = doc.add_paragraph(
        '外键关系定义了表之间的引用完整性约束，确保数据的一致性。'
    )
    doc.add_paragraph()

    # Foreign keys summary
    fk_table = doc.add_table(rows=1, cols=4)
    fk_table.style = 'Light Grid Accent 1'
    add_table_header(fk_table, ['子表', '外键字段', '父表', '删除策略'])

    foreign_keys = [
        ('users', 'group_id', 'groups.id', 'SET NULL'),
        ('tickets', 'template_id', 'templates.id', 'RESTRICT'),
        ('tickets', 'assigned_to', 'users.id', 'RESTRICT'),
        ('tickets', 'created_by', 'users.id', 'RESTRICT'),
        ('ticket_comments', 'ticket_id', 'tickets.id', 'CASCADE'),
        ('ticket_comments', 'user_id', 'users.id', 'RESTRICT'),
        ('template_steps', 'template_id', 'templates.id', 'CASCADE'),
        ('template_fields', 'step_id', 'template_steps.id', 'CASCADE'),
    ]

    for fk in foreign_keys:
        row = fk_table.add_row()
        for idx, value in enumerate(fk):
            row.cells[idx].text = value
            row.cells[idx].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()

    # Cascade behavior explanation
    doc.add_heading('删除策略说明', level=2)
    cascade_para = doc.add_paragraph()
    cascade_para.add_run('• CASCADE: ').bold = True
    cascade_para.add_run('级联删除 - 删除父记录时自动删除子记录\n')
    cascade_para.add_run('• RESTRICT: ').bold = True
    cascade_para.add_run('限制删除 - 存在子记录时不允许删除父记录\n')
    cascade_para.add_run('• SET NULL: ').bold = True
    cascade_para.add_run('设置为空 - 删除父记录时将外键设置为NULL')

    # Page break
    doc.add_page_break()

    # Indexes Section
    doc.add_heading('5. 索引说明', level=1)

    index_intro = doc.add_paragraph(
        '索引用于优化查询性能。系统为主键、唯一约束和外键自动创建索引。'
    )
    doc.add_paragraph()

    # Index types
    doc.add_heading('索引类型', level=2)
    index_types = doc.add_paragraph()
    index_types.add_run('• PRIMARY KEY: ').bold = True
    index_types.add_run('主键索引 - 唯一且不允许NULL\n')
    index_types.add_run('• UNIQUE INDEX: ').bold = True
    index_types.add_run('唯一索引 - 值必须唯一\n')
    index_types.add_run('• INDEX: ').bold = True
    index_types.add_run('普通索引 - 加速查询')

    doc.add_paragraph()

    # Performance recommendations
    doc.add_heading('性能建议', level=2)
    perf_para = doc.add_paragraph()
    perf_para.add_run('1. ').bold = True
    perf_para.add_run('所有UUID主键已建立索引\n')
    perf_para.add_run('2. ').bold = True
    perf_para.add_run('用户名、邮箱等常用查询字段已建立唯一索引\n')
    perf_para.add_run('3. ').bold = True
    perf_para.add_run('外键字段已建立索引以优化JOIN操作\n')
    perf_para.add_run('4. ').bold = True
    perf_para.add_run('工单状态字段建议添加索引以优化状态过滤查询')

    # Page break
    doc.add_page_break()

    # Design Notes
    doc.add_heading('6. 设计说明', level=1)

    design_notes = """
主键设计
• 所有表使用VARCHAR(36)存储UUID作为主键
• UUID确保分布式环境下的全局唯一性
• 便于数据迁移和同步

时间戳管理
• created_at: 记录创建时间，默认为当前时间
• updated_at: 记录更新时间，自动更新
• 所有时间戳使用DATETIME类型，存储UTC时间

JSON字段应用
• completed_steps: 存储已完成步骤的ID列表
• step_data: 存储步骤字段的动态数据
• tags: 存储分组标签列表
• related_ticket_ids: 存储关联工单ID

数据完整性
• 使用枚举类型约束状态、角色等字段
• 外键约束确保引用完整性
• 适当的级联删除策略保证数据一致性
• NOT NULL约束防止关键字段为空

扩展性考虑
• JSON字段支持灵活的数据扩展
• 模板系统支持自定义工作流程
• 站点级别配置支持差异化SLA管理
"""

    for line in design_notes.strip().split('\n'):
        if line and not line.startswith(' '):
            doc.add_heading(line, level=2)
        else:
            doc.add_paragraph(line)

    # Save document
    output_file = '/home/user/iGreen_ticketingsys/iGreen数据库表结构文档.docx'
    doc.save(output_file)
    print(f'✅ Word文档已生成: {output_file}')
    return output_file


if __name__ == '__main__':
    create_database_documentation()
