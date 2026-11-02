import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(page_title="마피아 게임 사회자 콘솔", page_icon="🕵️‍♂️", layout="wide")

# 세션 상태 초기화
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "phase" not in st.session_state:
    st.session_state.phase = "대기"  # 대기, 낮(토론), 낮(투표), 밤
if "day_count" not in st.session_state:
    st.session_state.day_count = 1
if "players" not in st.session_state:
    st.session_state.players = {}  # {이름: {"role": 직업, "alive": True/False}}
if "chat_logs" not in st.session_state:
    st.session_state.chat_logs = []
if "system_logs" not in st.session_state:
    st.session_state.system_logs = []
if "night_actions" not in st.session_state:
    st.session_state.night_actions = {"mafia_target": None, "doctor_target": None, "police_target": None}

# 사이드바: 게임 설정 및 사회자 컨트롤러
st.sidebar.title("🎮 사회자 컨트롤러")

if not st.session_state.game_started:
    st.sidebar.subheader("⚙️ 게임 설정")
    total_players = st.sidebar.number_input("총 참여 인원", min_value=4, max_value=30, value=20)
    mafia_count = st.sidebar.number_input("마피아 수", min_value=1, max_value=total_players // 2, value=2)
    doctor_count = st.sidebar.number_input("의사 수", min_value=0, max_value=total_players // 4, value=1)
    police_count = st.sidebar.number_input("경찰 수", min_value=0, max_value=total_players // 4, value=1)

    citizen_count = total_players - (mafia_count + doctor_count + police_count)
    st.sidebar.info(f"👨‍🌾 시민 수: {citizen_count}명")

    if citizen_count < 0:
        st.sidebar.error("특수 직업 수가 총 인원보다 많습니다!")
    else:
        if st.sidebar.button("🚀 게임 시작", use_container_width=True):
            # 직업 생성 및 분배
            roles = (
                ["마피아"] * mafia_count +
                ["의사"] * doctor_count +
                ["경찰"] * police_count +
                ["시민"] * citizen_count
            )
            random.shuffle(roles)

            st.session_state.players = {
                f"Player_{i+1}": {"role": roles[i], "alive": True}
                for i in range(total_players)
            }
            st.session_state.game_started = True
            st.session_state.phase = "낮(토론)"
            st.session_state.day_count = 1
            st.session_state.chat_logs = []
            st.session_state.system_logs = [f"📢 {st.session_state.day_count}번째 낮이 밝았습니다. AI 토론을 시작합니다."]
            st.rerun()

else:
    st.sidebar.subheader("🔄 진행 제어")
    st.sidebar.write(f"현재 단계: **{st.session_state.phase}** ({st.session_state.day_count}일차)")

    if st.sidebar.button("🔄 게임 리셋", use_container_width=True):
        st.session_state.game_started = False
        st.rerun()

# 메인 화면
st.title("🕵️‍♂️ 마피아 게임 사회자 콘솔 (AI 20인 모드)")

if not st.session_state.game_started:
    st.warning("사이드바에서 직업 인원을 설정하고 '게임 시작' 버튼을 눌러주세요.")
else:
    col1, col2 = st.columns([1, 2])

    # 왼쪽 컬럼: 참가자 상태 확인판 (관전자/사회자 전용)
    with col1:
        st.subheader("👥 참가자 상태 (사회자 화면)")
        alive_mafia = sum(1 for p in st.session_state.players.values() if p['role'] == '마피아' and p['alive'])
        alive_citizens = sum(1 for p in st.session_state.players.values() if p['role'] != '마피아' and p['alive'])
        
        st.caption(f"생존: 마피아 {alive_mafia}명 | 시민팀 {alive_citizens}명")

        player_data = []
        for name, info in st.session_state.players.items():
            status = "🟢 생존" if info["alive"] else "💀 사망"
            player_data.append({"플레이어": name, "직업": info["role"], "상태": status})
        
        st.dataframe(player_data, use_container_width=True, height=500)

    # 오른쪽 컬럼: 게임 진행 영역
    with col2:
        st.subheader(f"☀️ Day {st.session_state.day_count} - {st.session_state.phase}")

        # 시스템 알림 로그
        for sys_log in st.session_state.system_logs[-3:]:
            st.info(sys_log)

        # 1. 낮(토론) 단계
        if st.session_state.phase == "낮(토론)":
            st.markdown("### 💬 AI 토론 현황")
            
            # AI 대화 생성 버튼
            if st.button("🤖 AI 대화 추가 진행"):
                alive_players = [name for name, p in st.session_state.players.items() if p["alive"]]
                speaker = random.choice(alive_players)
                target = random.choice([p for p in alive_players if p != speaker])
                
                # 시뮬레이션용 단순 AI 멘트
                dialogues = [
                    f"저는 선량한 시민입니다. {target}님이 좀 수상해 보여요.",
                    f"{target}님의 지난 언행이 약간 마피아 같지 않나요?",
                    "저는 진짜 시민입니다! 의심하지 말아주세요.",
                    f"지금 무턱대고 몰아가는 {target}님이 오히려 마피아일 가능성이 높습니다.",
                    "직업 있으신 분은 밤에 확인해주시고, 지금은 좀 더 지켜보죠."
                ]
                text = random.choice(dialogues)
                st.session_state.chat_logs.append(f"**{speaker}**: {text}")

            # 대화 로그 출력
            chat_container = st.container(height=300)
            with chat_container:
                for chat in st.session_state.chat_logs:
                    st.write(chat)

            if st.button("➡️ 토론 종료 후 투표로 이동", type="primary"):
                st.session_state.phase = "낮(투표)"
                st.rerun()

        # 2. 낮(투표) 단계
        elif st.session_state.phase == "낮(투표)":
            st.markdown("### 🗳️ AI 투표 진행")
            
            if st.button("🗳️ AI 전원 투표 실행"):
                alive_players = [name for name, p in st.session_state.players.items() if p["alive"]]
                votes = {name: 0 for name in alive_players}
                votes["무효표"] = 0

                # AI 무작위/임의 투표 계산
                for voter in alive_players:
                    # 20% 확률로 무효표, 80% 확률로 타인에게 투표
                    if random.random() < 0.2:
                        votes["무효표"] += 1
                    else:
                        target = random.choice([p for p in alive_players if p != voter])
                        votes[target] += 1

                st.write("📊 **투표 결과:**")
                st.json(votes)

                # 최다 득표자 선출 (무효표 제외 상위자 계산)
                max_votes = max([v for k, v in votes.items() if k != "무효표"] + [0])
                top_voted = [k for k, v in votes.items() if k != "무효표" and v == max_votes]

                if max_votes > votes["무효표"] and len(top_voted) == 1:
                    executed = top_voted[0]
                    st.session_state.players[executed]["alive"] = False
                    st.session_state.system_logs.append(f"⚖️ 투표 결과, [{executed}]님이 처형되었습니다.")
                else:
                    st.session_state.system_logs.append("⚖️ 동표가 나오거나 무효표가 많아 아무도 처형되지 않았습니다.")

                st.session_state.phase = "밤"
                st.rerun()

        # 3. 밤 단계
        elif st.session_state.phase == "밤":
            st.markdown("### 🌙 밤이 되었습니다.")
            st.caption("마피아, 의사, 경찰이 지목을 진행합니다.")

            alive_mafia = [n for n, p in st.session_state.players.items() if p["role"] == "마피아" and p["alive"]]
            alive_doctor = [n for n, p in st.session_state.players.items() if p["role"] == "의사" and p["alive"]]
            alive_police = [n for n, p in st.session_state.players.items() if p["role"] == "경찰" and p["alive"]]
            alive_all = [n for n, p in st.session_state.players.items() if p["alive"]]

            if st.button("🌙 밤 행동 시뮬레이션 처리"):
                # 마피아 표적 선택
                target_mafia = random.choice([p for p in alive_all if p not in alive_mafia]) if alive_mafia else None
                # 의사 표적 선택
                target_doctor = random.choice(alive_all) if alive_doctor else None
                # 경찰 조사 선택
                target_police = random.choice([p for p in alive_all if p not in alive_police]) if alive_police else None

                result_text = []

                # 의사의 구출 여부 확인
                if target_mafia:
                    if target_mafia == target_doctor:
                        result_text.append(f"🚑 의사가 마피아의 공격을 성공적으로 막아냈습니다!")
                    else:
                        st.session_state.players[target_mafia]["alive"] = False
                        result_text.append(f"💀 밤 사이에 [{target_mafia}]님이 마피아의 공격으로 사망했습니다.")
                else:
                    result_text.append("🌙 밤 사이에 아무 일도 일어나지 않았습니다.")

                # 경찰 조사 결과 기록 (사회자 확인용)
                if target_police:
                    is_mafia = st.session_state.players[target_police]["role"] == "마피아"
                    result_text.append(f"🔍 [경찰 조사] {target_police}님은 {'마피아' if is_mafia else '시민/특직'}입니다.")

                st.session_state.day_count += 1
                st.session_state.phase = "낮(토론)"
                st.session_state.system_logs.extend(result_text)
                st.session_state.chat_logs = []  # 다음날을 위해 대화 초기화
                st.rerun()

        # 승리 조건 검사
        alive_mafia_count = sum(1 for p in st.session_state.players.values() if p['role'] == '마피아' and p['alive'])
        alive_citizen_count = sum(1 for p in st.session_state.players.values() if p['role'] != '마피아' and p['alive'])

        if alive_mafia_count == 0:
            st.balloons()
            st.success("🎉 모든 마피아가 소탕되었습니다! **시민팀 승리!**")
        elif alive_mafia_count >= alive_citizen_count and alive_mafia_count > 0:
            st.error("🩸 마피아 수가 시민 수와 같거나 많아졌습니다. **마피아팀 승리!**")
