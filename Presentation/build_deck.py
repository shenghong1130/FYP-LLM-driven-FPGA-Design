from pathlib import Path
import sys, hashlib, json
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.pptx_deps'))
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.xmlchemy import OxmlElement

OUT=Path(__file__).resolve().parent
OUT.joinpath('Preview').mkdir(exist_ok=True)
prs=Presentation(); prs.slide_width=Inches(13.333333); prs.slide_height=Inches(7.5)
PUR='82318E'; INK='24283B'; GRAY='64748B'; LIGHT='F4EEF7'; PALE='F5F6F8'; BLUE='EDF2F7'
def box(s,x,y,w,h,fill,stroke=None):
 q=s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
 q.fill.solid(); q.fill.fore_color.rgb=RGBColor.from_string(fill)
 q.line.fill.background() if stroke is None else None
 q._element.spPr.append(OxmlElement('a:effectLst'))
 if stroke: q.line.color.rgb=RGBColor.from_string(stroke); q.line.width=Pt(1)
 return q
def text(s,x,y,w,h,t,size=15,color=INK,bold=False,align=None):
 q=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); tf=q.text_frame
 tf.clear(); tf.word_wrap=True
 tf.margin_left=tf.margin_right=Inches(.02); tf.margin_top=tf.margin_bottom=0
 for i,line in enumerate(t.split('\n')):
  p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.text=line
  p.font.name='Microsoft YaHei'; p.font.size=Pt(size); p.font.bold=bold; p.font.color.rgb=RGBColor.from_string(color)
  p.space_after=Pt(3); p.space_before=Pt(0)
  if align is not None: p.alignment=align
 return q
def line(s,x1,y1,x2,y2,color=GRAY,arrow=True,width=1.5):
 q=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1),Inches(y1),Inches(x2),Inches(y2))
 q.line.color.rgb=RGBColor.from_string(color); q.line.width=Pt(width)
 q._element.spPr.append(OxmlElement('a:effectLst'))
 if arrow:
  el=OxmlElement('a:tailEnd'); el.set('type','triangle'); q.line._get_or_add_ln().append(el)
 return q
def center(s,x,y,w,h,t,size=15,fill=LIGHT,color=INK,bold=False):
 box(s,x,y,w,h,fill); return text(s,x+.08,y+.09,w-.16,h-.10,t,size,color,bold,PP_ALIGN.CENTER)
def base(title,num):
 s=prs.slides.add_slide(prs.slide_layouts[6]); box(s,.45,.39,.06,.43,PUR)
 text(s,.65,.37,12.1,.52,title,27,PUR,True)
 line(s,.48,1.02,12.85,1.02,'DED7E3',False,1)
 text(s,.5,7.15,11,.2,'大模型驱动的FPGA智能设计方法研究',11,GRAY)
 text(s,12.2,7.13,.6,.22,f'{num:02d} / 02',11,GRAY,align=PP_ALIGN.RIGHT)
 return s

s=base('大模型驱动的FPGA智能设计：研究目标与技术路线',1)
text(s,.52,1.22,4.25,.35,'研究目标',19,PUR,True)
text(s,.52,1.7,4.15,.92,'构建设计生成、工具调用与反馈优化的自动化闭环，提升FPGA设计迭代效率',17)
for y,n,title,body in [
 (2.92,'01','工具交互机制构建','封装仿真、综合、布局布线与板级测试\n提取功能、资源和时序反馈'),
 (4.04,'02','反馈驱动设计优化','分阶段评估与候选筛选\n复用历史结果，减少无效探索'),
 (5.16,'03','NPU案例与FPGA验证','基于已有参数化NPU优化并行度、\n缓存及调度，开展板级与对比实验')]:
 text(s,.52,y,.43,.3,n,17,PUR,True); text(s,1.04,y,3.7,.33,title,18,INK,True)
 text(s,1.04,y+.43,3.75,.62,body,14,GRAY)
line(s,4.9,1.25,4.9,6.55,'DED7E3',False,1)
cx=8.23; x=5.35; w=5.76
center(s,x,1.2,w,.4,'应用需求 / FPGA设计约束',14,PALE)
line(s,cx,1.6,cx,1.79)
center(s,x,1.8,w,.62,'大语言模型 LLM',20,PUR,'FFFFFF',True)
text(s,5.4,2.44,5.66,.25,'方案生成与参数调整',12.5,GRAY,align=PP_ALIGN.CENTER)
line(s,cx,2.72,cx,2.88)
box(s,x,2.89,w,.72,LIGHT)
text(s,x+.1,2.94,w-.2,.29,'参数化 NPU 设计',17,PUR,True,PP_ALIGN.CENTER)
text(s,x+.1,3.3,w-.2,.24,'计算阵列     片上缓存     数据调度',14,INK,align=PP_ALIGN.CENTER)
line(s,cx,3.61,cx,3.8)
box(s,x,3.81,w,.95,BLUE,GRAY)
text(s,x+.1,3.86,w-.2,.3,'FPGA EDA工具链',18,INK,True,PP_ALIGN.CENTER)
for xx,label in [(5.55,'功能仿真'),(7.46,'逻辑综合'),(9.37,'布局布线')]:
 center(s,xx,4.28,1.55,.35,label,14,'FFFFFF')
line(s,7.13,4.47,7.41,4.47); line(s,9.04,4.47,9.32,4.47)
line(s,cx,4.76,cx,4.96)
center(s,x,4.97,w,.45,'评估结果：功能检查 / 资源占用 / 时序性能',14,PALE)
line(s,cx,5.42,cx,5.62)
center(s,x,5.63,w,.56,'结果解析 / 候选方案筛选',17,LIGHT,PUR,True)
line(s,11.11,5.91,12.38,5.91,PUR,False,2.4)
line(s,12.38,5.91,12.38,2.11,PUR,False,2.4)
line(s,12.38,2.11,11.11,2.11,PUR,True,2.4)
text(s,11.3,3.05,.9,1.3,'结构化\n反馈\n\n迭代优化',13,PUR,True,PP_ALIGN.CENTER)
line(s,cx,6.19,cx,6.53,GRAY)
text(s,8.38,6.25,2.5,.24,'选取代表性方案',12,GRAY)
center(s,6.48,6.54,3.5,.4,'FPGA 板级验证',15,BLUE,INK,True)
s.notes_slide.notes_text_frame.text='正式课题依据：项目目录中的《毕设题目.docx》。目标是利用大模型辅助FPGA硬件设计与优化。以面向轻量Transformer推理的已有参数化NPU作为验证对象。功能仿真和性能估计先筛查，再对有潜力的候选设计开展综合与布局布线。板级验证用于代表性方案，位于主迭代流程之外。'

s=base('研究计划与当前进展',2)
text(s,.52,1.2,8,.35,'研究计划',19,PUR,True)
stages=[('文献调研','调研大模型辅助EDA\n熟悉流程与NPU原型'),('工具构建','Python/Tcl调用与解析\n建立检查和实验记录'),('优化方法','反馈调整与分阶段筛选\n历史复用及终止条件'),('实验验证','优化NPU参数配置\n基线对比及板级测试'),('论文总结','分析质量、效率与开销\n整理实验并完成论文')]
for i,(title,body) in enumerate(stages):
 xx=.52+i*2.5
 box(s,xx,1.86,2.28,1.37,LIGHT if i%2==0 else PALE)
 text(s,xx+.13,1.97,.4,.32,f'{i+1:02d}',18,PUR,True)
 text(s,xx+.58,1.98,1.6,.31,title,18,INK,True)
 text(s,xx+.12,2.5,2.08,.62,body,13.5,GRAY)
 if i<4: line(s,xx+2.3,2.16,xx+2.47,2.16,PUR,True)
text(s,.54,3.43,12.1,.28,'实验对比：人工配置与传统搜索基线，保持应用负载、设计约束和评估预算一致',14,GRAY)
line(s,.52,3.93,12.8,3.93,'DED7E3',False,1)
text(s,.52,4.13,5.9,.34,'当前准备与已有基础',19,PUR,True)
text(s,.53,4.65,5.8,.29,'课题准备（前期阶段）',16,INK,True)
text(s,.53,5.04,5.8,.59,'已明确研究目标及三项核心研究内容\n初步梳理大模型、EDA工具与FPGA设计的关系',14.5,GRAY)
text(s,.53,5.83,5.8,.29,'已有技术基础（过往实践）',16,INK,True)
text(s,.53,6.23,5.8,.75,'Python、C/C++、Linux、Git及FPGA基础\nKV260、PYNQ、Overlay、MMIO、DMA实践\n软硬件交互、板级部署与自动化脚本经验',14,GRAY)
line(s,6.52,4.17,6.52,6.97,'DED7E3',False,1)
text(s,6.83,4.13,5.9,.34,'下一步工作',19,PUR,True)
for yy,n,ti,bd in [
 (4.66,'01','文献与技术调研','学习大模型辅助RTL/FPGA设计方法'),
 (5.25,'02','熟悉设计工具链','学习Vivado仿真、综合、布局布线及报告提取'),
 (5.84,'03','分析NPU原型','获取原型，梳理阵列、缓存与调度的可调参数'),
 (6.43,'04','建立最小闭环','先贯通参数修改、EDA评估与结果提取，再接入LLM')]:
 text(s,6.84,yy,.36,.26,n,14,PUR,True)
 text(s,7.29,yy,5.45,.28,ti,15.5,INK,True)
 text(s,7.29,yy+.31,5.45,.28,bd,13,GRAY)
s.notes_slide.notes_text_frame.text='研究计划依据《毕设题目.docx》，当前准备与过往技术基础依据用户提供的信息。当前仍为前期准备，尚未宣称完成Agent、EDA自动化平台、NPU优化实验或本课题板级验证。阶段编号仅表示顺序，不设置未经确认的日期。实验将比较功能通过率、推理延迟、吞吐率与资源占用，并统计工具调用次数和探索总耗时。'
dest=OUT/'本科毕设_目标计划进展.pptx'
prs.save(dest)
assert len(prs.slides)==2
for slide in prs.slides:
 for shape in slide.shapes:
  assert shape.left>=0 and shape.top>=0 and shape.left+shape.width<=prs.slide_width+10 and shape.top+shape.height<=prs.slide_height+10
  if shape.has_text_frame:
   for p in shape.text_frame.paragraphs:
    for r in p.runs:
     assert r.font.size is None or r.font.size.pt>=11
print(dest)
