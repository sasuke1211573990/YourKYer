import random
from sqlalchemy.orm import Session
from . import models, database

def init_db(db: Session):
    # 50 Mainstream Universities Data
    universities_data = [
        {"name": "清华大学", "location": "北京", "level": "985", "website": "https://www.tsinghua.edu.cn"},
        {"name": "北京大学", "location": "北京", "level": "985", "website": "https://www.pku.edu.cn"},
        {"name": "浙江大学", "location": "杭州", "level": "985", "website": "https://www.zju.edu.cn"},
        {"name": "上海交通大学", "location": "上海", "level": "985", "website": "https://www.sjtu.edu.cn"},
        {"name": "复旦大学", "location": "上海", "level": "985", "website": "https://www.fudan.edu.cn"},
        {"name": "南京大学", "location": "南京", "level": "985", "website": "https://www.nju.edu.cn"},
        {"name": "中国科学技术大学", "location": "合肥", "level": "985", "website": "https://www.ustc.edu.cn"},
        {"name": "华中科技大学", "location": "武汉", "level": "985", "website": "https://www.hust.edu.cn"},
        {"name": "武汉大学", "location": "武汉", "level": "985", "website": "https://www.whu.edu.cn"},
        {"name": "西安交通大学", "location": "西安", "level": "985", "website": "https://www.xjtu.edu.cn"},
        {"name": "哈尔滨工业大学", "location": "哈尔滨", "level": "985", "website": "https://www.hit.edu.cn"},
        {"name": "中山大学", "location": "广州", "level": "985", "website": "https://www.sysu.edu.cn"},
        {"name": "北京航空航天大学", "location": "北京", "level": "985", "website": "https://www.buaa.edu.cn"},
        {"name": "四川大学", "location": "成都", "level": "985", "website": "https://www.scu.edu.cn"},
        {"name": "同济大学", "location": "上海", "level": "985", "website": "https://www.tongji.edu.cn"},
        {"name": "南开大学", "location": "天津", "level": "985", "website": "https://www.nankai.edu.cn"},
        {"name": "东南大学", "location": "南京", "level": "985", "website": "https://www.seu.edu.cn"},
        {"name": "中国人民大学", "location": "北京", "level": "985", "website": "https://www.ruc.edu.cn"},
        {"name": "北京理工大学", "location": "北京", "level": "985", "website": "https://www.bit.edu.cn"},
        {"name": "天津大学", "location": "天津", "level": "985", "website": "https://www.tju.edu.cn"},
        {"name": "山东大学", "location": "济南", "level": "985", "website": "https://www.sdu.edu.cn"},
        {"name": "中南大学", "location": "长沙", "level": "985", "website": "https://www.csu.edu.cn"},
        {"name": "吉林大学", "location": "长春", "level": "985", "website": "https://www.jlu.edu.cn"},
        {"name": "西北工业大学", "location": "西安", "level": "985", "website": "https://www.nwpu.edu.cn"},
        {"name": "大连理工大学", "location": "大连", "level": "985", "website": "https://www.dlut.edu.cn"},
        {"name": "厦门大学", "location": "厦门", "level": "985", "website": "https://www.xmu.edu.cn"},
        {"name": "湖南大学", "location": "长沙", "level": "985", "website": "https://www.hnu.edu.cn"},
        {"name": "重庆大学", "location": "重庆", "level": "985", "website": "https://www.cqu.edu.cn"},
        {"name": "兰州大学", "location": "兰州", "level": "985", "website": "https://www.lzu.edu.cn"},
        {"name": "电子科技大学", "location": "成都", "level": "985", "website": "https://www.uestc.edu.cn"},
        {"name": "华南理工大学", "location": "广州", "level": "985", "website": "https://www.scut.edu.cn"},
        {"name": "中国农业大学", "location": "北京", "level": "985", "website": "https://www.cau.edu.cn"},
        {"name": "东北大学", "location": "沈阳", "level": "985", "website": "https://www.neu.edu.cn"},
        {"name": "华东师范大学", "location": "上海", "level": "985", "website": "https://www.ecnu.edu.cn"},
        {"name": "北京师范大学", "location": "北京", "level": "985", "website": "https://www.bnu.edu.cn"},
        {"name": "中国海洋大学", "location": "青岛", "level": "985", "website": "https://www.ouc.edu.cn"},
        {"name": "中央民族大学", "location": "北京", "level": "985", "website": "https://www.muc.edu.cn"},
        {"name": "国防科技大学", "location": "长沙", "level": "985", "website": "https://www.nudt.edu.cn"},
        {"name": "西北农林科技大学", "location": "杨凌", "level": "985", "website": "https://www.nwafu.edu.cn"},
        {"name": "郑州大学", "location": "郑州", "level": "211", "website": "https://www.zzu.edu.cn"},
        {"name": "云南大学", "location": "昆明", "level": "211", "website": "https://www.ynu.edu.cn"},
        {"name": "新疆大学", "location": "乌鲁木齐", "level": "211", "website": "https://www.xju.edu.cn"},
        {"name": "上海大学", "location": "上海", "level": "211", "website": "https://www.shu.edu.cn"},
        {"name": "苏州大学", "location": "苏州", "level": "211", "website": "https://www.suda.edu.cn"},
        {"name": "南京理工大学", "location": "南京", "level": "211", "website": "https://www.njust.edu.cn"},
        {"name": "武汉理工大学", "location": "武汉", "level": "211", "website": "https://www.whut.edu.cn"},
        {"name": "西南大学", "location": "重庆", "level": "211", "website": "https://www.swu.edu.cn"},
        {"name": "华中师范大学", "location": "武汉", "level": "211", "website": "https://www.ccnu.edu.cn"},
        {"name": "西安电子科技大学", "location": "西安", "level": "211", "website": "https://www.xidian.edu.cn"},
        {"name": "北京交通大学", "location": "北京", "level": "211", "website": "https://www.bjtu.edu.cn"}
    ]

    for uni_data in universities_data:
        uni = db.query(models.University).filter(models.University.name == uni_data["name"]).first()
        if not uni:
            uni = models.University(
                name=uni_data["name"],
                location=uni_data["location"],
                level=uni_data["level"],
                website=uni_data["website"],
                admission_guide=f"{uni_data['name']} 2024年硕士研究生招生简章...",
                recruit_policy=f"{uni_data['name']} 2024年硕士研究生招生政策..."
            )
            db.add(uni)
            
            # Add some dummy majors for each university
            majors = [
                {"name": "计算机科学与技术", "code": "081200"},
                {"name": "软件工程", "code": "083500"},
                {"name": "电子信息", "code": "085400"},
                {"name": "工商管理", "code": "125100"}
            ]
            
            for m_data in majors:
                major = models.Major(
                    university=uni,
                    name=m_data["name"],
                    code=m_data["code"],
                    exam_subjects="思想政治理论, 英语一, 数学一, 专业课",
                    score_line='{"2023": 350, "2022": 345, "2021": 340}'
                )
                db.add(major)
    
    db.commit()

if __name__ == "__main__":
    db = database.SessionLocal()
    init_db(db)
    print("Database initialized with 50 universities and sample majors.")
    db.close()
