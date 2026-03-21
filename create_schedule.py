#!/usr/bin/env python3
"""
排班表生成器
- 每四天一个周期
- 第1天：24小时值班（值班日）
- 第2天：正常上班
- 第3天：正常上班，除非遇到周末（星期六、星期日）才休息
- 第4天：正常休息
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime, timedelta
import calendar

# 创建工作簿
wb = Workbook()
ws = wb.active
ws.title = "排班表"

# 隐藏网格线
ws.sheet_view.showGridLines = False

# 定义颜色
header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
header_font = Font(bold=True, color="FFFFFF", size=12)
title_font = Font(bold=True, size=16)
duty_fill = PatternFill(start_color="FF6B6B", end_color="FF6B6B", fill_type="solid")  # 红色 - 值班日
work_fill = PatternFill(start_color="4ECDC4", end_color="4ECDC4", fill_type="solid")  # 青色 - 正常上班
weekend_work_fill = PatternFill(start_color="95E1D3", end_color="95E1D3", fill_type="solid")  # 浅绿 - 周末上班
rest_fill = PatternFill(start_color="DDA0DD", end_color="DDA0DD", fill_type="solid")  # 紫色 - 休息
weekend_rest_fill = PatternFill(start_color="E6E6FA", end_color="E6E6FA", fill_type="solid")  # 浅紫 - 周末休息

thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

# 起始日期 - 从2025年1月1日开始（可以根据需要修改）
start_date = datetime(2025, 1, 1)

# 排班规则函数
def get_schedule_status(day_in_cycle, weekday):
    """
    day_in_cycle: 1-4 表示在4天周期中的第几天
    weekday: 0=周一, 1=周二, ..., 5=周六, 6=周日
    返回: (状态, 状态描述)
    """
    if day_in_cycle == 1:
        return ("值班日", "24小时值班", duty_fill)
    elif day_in_cycle == 2:
        return ("上班", "正常上班", work_fill)
    elif day_in_cycle == 3:
        # 第三天：正常上班，除非遇到周末才休息
        if weekday >= 5:  # 周六或周日
            return ("休息", "周末休息", weekend_rest_fill)
        else:
            return ("上班", "正常上班", weekend_work_fill)
    elif day_in_cycle == 4:
        return ("休息", "正常休息", rest_fill)
    return ("", "", None)

# 生成排班数据
days_in_months = [
    (2025, 1, 31),
    (2025, 2, 28),
    (2025, 3, 31),
    (2025, 4, 30),
    (2025, 5, 31),
    (2025, 6, 30),
    (2025, 7, 31),
    (2025, 8, 31),
    (2025, 9, 30),
    (2025, 10, 31),
    (2025, 11, 30),
    (2025, 12, 31),
]

# 先计算全年的数据用于统计
year_schedule = []
for i in range(365):
    current_date = start_date + timedelta(days=i)
    day_in_cycle = (i % 4) + 1
    weekday = current_date.weekday()  # 0=周一, 6=周日
    status, desc, fill = get_schedule_status(day_in_cycle, weekday)
    year_schedule.append({
        'date': current_date,
        'day': i + 1,
        'cycle': day_in_cycle,
        'weekday': weekday,
        'weekday_name': ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][weekday],
        'status': status,
        'desc': desc,
        'fill': fill
    })

# 统计全年休息天数
total_rest_days = sum(1 for day in year_schedule if day['status'] == '休息')
total_duty_days = sum(1 for day in year_schedule if day['status'] == '值班日')
total_work_days = sum(1 for day in year_schedule if day['status'] == '上班')

print(f"全年统计:")
print(f"  值班日: {total_duty_days} 天")
print(f"  正常上班: {total_work_days} 天")
print(f"  休息日: {total_rest_days} 天")
print(f"  合计: {total_duty_days + total_work_days + total_rest_days} 天")

# 创建两个月的排班表（假设用户需要1月和2月）
# 可以根据需要修改为其他月份
two_months = [
    (2025, 1, "2025年1月"),
    (2025, 2, "2025年2月"),
]

# 写入标题
ws['B2'] = "排班表（2025年1月-2月）"
ws['B2'].font = title_font
ws.merge_cells('B2:H2')
ws['B2'].alignment = Alignment(horizontal='center', vertical='center')

# 写入统计信息
ws['B4'] = f"全年可休息天数: {total_rest_days} 天"
ws['B4'].font = Font(bold=True, size=11)
ws.merge_cells('B4:E4')

ws['B5'] = f"全年值班天数: {total_duty_days} 天"
ws['B5'].font = Font(bold=True, size=11)
ws.merge_cells('B5:E5')

ws['B6'] = f"全年上班天数: {total_work_days} 天"
ws['B6'].font = Font(bold=True, size=11)
ws.merge_cells('B6:E6')

# 写入表头
headers = ['日期', '星期', '第几天班', '状态', '说明']
header_row = 8

for col, header in enumerate(headers, start=2):
    cell = ws.cell(row=header_row, column=col, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell.border = thin_border

# 筛选出1月和2月的数据
two_months_data = [day for day in year_schedule 
                   if day['date'].month in [1, 2]]

# 写入数据
current_row = header_row + 1
for day_data in two_months_data:
    ws.cell(row=current_row, column=2, value=day_data['date'].strftime('%Y-%m-%d'))
    ws.cell(row=current_row, column=3, value=day_data['weekday_name'])
    ws.cell(row=current_row, column=4, value=day_data['cycle'])
    ws.cell(row=current_row, column=5, value=day_data['status'])
    ws.cell(row=current_row, column=6, value=day_data['desc'])
    
    # 设置状态单元格的填充颜色
    if day_data['fill']:
        ws.cell(row=current_row, column=5).fill = day_data['fill']
    
    # 设置边框和对齐
    for col in range(2, 7):
        ws.cell(row=current_row, column=col).border = thin_border
        ws.cell(row=current_row, column=col).alignment = Alignment(horizontal='center', vertical='center')
    
    current_row += 1

# 设置列宽
ws.column_dimensions['B'].width = 15
ws.column_dimensions['C'].width = 10
ws.column_dimensions['D'].width = 12
ws.column_dimensions['E'].width = 12
ws.column_dimensions['F'].width = 15

# 添加图例
legend_row = current_row + 2
ws[f'B{legend_row}'] = "图例："
ws[f'B{legend_row}'].font = Font(bold=True)

legend_items = [
    (duty_fill, "值班日（24小时）"),
    (work_fill, "正常上班"),
    (weekend_work_fill, "周末上班"),
    (rest_fill, "正常休息"),
    (weekend_rest_fill, "周末休息"),
]

for i, (fill, desc) in enumerate(legend_items):
    row = legend_row + 1 + i
    ws[f'B{row}'].fill = fill
    ws[f'B{row}'].border = thin_border
    ws[f'C{row}'] = desc
    ws[f'C{row}'].alignment = Alignment(horizontal='left', vertical='center')

# 创建全年统计表
ws2 = wb.create_sheet("全年统计")
ws2.sheet_view.showGridLines = False

ws2['B2'] = "2025年全年排班统计"
ws2['B2'].font = title_font
ws2.merge_cells('B2:F2')

# 月度统计
ws2['B4'] = "月度统计"
ws2['B4'].font = Font(bold=True, size=12)

monthly_headers = ['月份', '值班日', '上班', '休息', '合计']
for col, header in enumerate(monthly_headers, start=2):
    cell = ws2.cell(row=5, column=col, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell.border = thin_border

month_stats = {}
for month in range(1, 13):
    month_data = [day for day in year_schedule if day['date'].month == month]
    duty = sum(1 for d in month_data if d['status'] == '值班日')
    work = sum(1 for d in month_data if d['status'] == '上班')
    rest = sum(1 for d in month_data if d['status'] == '休息')
    month_stats[month] = {'duty': duty, 'work': work, 'rest': rest}
    
    row = 5 + month
    month_name = f"{month}月"
    ws2.cell(row=row, column=2, value=month_name)
    ws2.cell(row=row, column=3, value=duty)
    ws2.cell(row=row, column=4, value=work)
    ws2.cell(row=row, column=5, value=rest)
    ws2.cell(row=row, column=6, value=duty + work + rest)
    
    for col in range(2, 7):
        ws2.cell(row=row, column=col).border = thin_border
        ws2.cell(row=row, column=col).alignment = Alignment(horizontal='center', vertical='center')

# 年度总计
total_row = 5 + 13
ws2[f'B{total_row}'] = "全年总计"
ws2[f'B{total_row}'].font = Font(bold=True)
ws2[f'C{total_row}'] = total_duty_days
ws2[f'C{total_row}'].font = Font(bold=True)
ws2[f'D{total_row}'] = total_work_days
ws2[f'D{total_row}'].font = Font(bold=True)
ws2[f'E{total_row}'] = total_rest_days
ws2[f'E{total_row}'].font = Font(bold=True)
ws2[f'F{total_row}'] = 365
ws2[f'F{total_row}'].font = Font(bold=True)

for col in range(2, 7):
    ws2.cell(row=total_row, column=col).border = thin_border
    ws2.cell(row=total_row, column=col).alignment = Alignment(horizontal='center', vertical='center')

# 设置列宽
ws2.column_dimensions['B'].width = 12
ws2.column_dimensions['C'].width = 12
ws2.column_dimensions['D'].width = 12
ws2.column_dimensions['E'].width = 12
ws2.column_dimensions['F'].width = 12

# 保存文件
output_file = "排班表.xlsx"
wb.save(output_file)
print(f"\n排班表已保存到: {output_file}")
