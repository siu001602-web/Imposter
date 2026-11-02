import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AI 마피아 게임 - 사회자 패널",
    page_icon="🕵️",
    layout="wide"
)

html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI 마피아 게임 - 사회자 패널</title>
  <style>
    :root {
      --bg-color: #0f172a;
      --panel-bg: #1e293b;
      --accent-color: #e11d48;
      --text-main: #f8fafc;
      --border-color: #334155;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }

    body {
      background-color: var(--bg-color);
      color: var(--text-main);
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    header {
      background-color: var(--panel-bg);
      padding: 20px;
      border-radius: 12px;
      border: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 15px;
    }

    .setup-panel {
      display: flex;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
    }

    .input-group {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    input[type="number"] {
      width: 55px;
      padding: 6px 8px;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      background-color: #0f172a;
      color: #fff;
      font-weight: bold;
      text-align: center;
    }

    .btn {
      padding: 8px 16px;
      border-radius: 6px;
      border: none;
      font-weight: bold;
      cursor: pointer;
      transition: all 0.2s;
    }

    .btn-primary { background-color: #2563eb; color: white; }
    .btn-danger { background-color: #e11d48; color: white; }
    .btn-warning { background-color: #d97706; color: white; }
    .btn-success { background-color: #059669; color: white; }
    .btn:disabled { opacity: 0.4; cursor: not-allowed; }
    .btn:hover:not(:disabled) { opacity: 0.9; transform: translateY(-1px); }

    .game-status-bar {
      display: flex;
      gap: 20px;
      background-color: var(--panel-bg);
      padding: 15px 20px;
      border-radius: 12px;
      border: 1px solid var(--border-color);
      align-items: center;
      font-size: 1.1rem;
    }

    .phase-badge {
      padding: 4px 12px;
      border-radius: 20px;
      font-weight: bold;
    }
    .phase-night { background-color: #312e81; color: #a5b4fc; }
    .phase-day { background-color: #78350f; color: #fde68a; }

    .main-content {
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 20px;
    }

    @media (max-width: 1024px) {
      .main-content { grid-template-columns: 1fr; }
    }

    .grid-players {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(135px, 1fr));
      gap: 12px;
    }

    .player-card {
      background-color: var(--panel-bg);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 10px;
      text-align: center;
      position: relative;
    }

    .player-card.dead {
      opacity: 0.35;
      background-color: #111;
      border-color: #444;
    }

    .player-card.revealed {
      border: 2px solid #38bdf8;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
    }

    .player-card .role {
      font-size: 0.78rem;
      margin-top: 4px;
      padding: 2px 6px;
      border-radius: 4px;
      display: inline-block;
    }

    .role-mafia { background: #881337; color: #fecdd3; }
    .role-assassin { background: #581c87; color: #f0abfc; }
    .role-doctor { background: #065f46; color: #a7f3d0; }
    .role-police { background: #1e40af; color: #bfdbfe; }
    .role-citizen { background: #374151; color: #e5e7eb; }

    .reveal-badge {
      font-size: 0.7rem;
      background-color: #0284c7;
      color: white;
      padding: 2px 5px;
      border-radius: 4px;
      margin-top: 3px;
      display: inline-block;
    }

    .log-container {
      background-color: var(--panel-bg);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 15px;
      display: flex;
      flex-direction: column;
      height: 600px;
    }

    .log-messages {
      flex: 1;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: 10px;
      padding-right: 5px;
    }

    .log-item {
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 0.9rem;
      background: #0f172a;
      line-height: 1.4;
      animation: fadeIn 0.3s ease-in-out;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .log-system { border-left: 3px solid #2563eb; }
    .log-chat { border-left: 3px solid #10b981; }
    .log-secret { border-left: 3px solid #e11d48; color: #fda4af; }
    .log-reveal { border-left: 3px solid #38bdf8; background: #0c4a6e; color: #e0f2fe; }

    .controls-panel {
      display: flex;
      gap: 10px;
      margin-top: 10px;
      flex-wrap: wrap;
    }
  </style>
</head>
<body>

  <header>
    <h1>🕵️ AI 마피아 게임 사회자 패널 (암살자 패치)</h1>
    <div class="setup-panel">
      <div class="input-group">
        <label>마피아:</label>
        <input type="number" id="count-mafia" value="2" min="1" max="5">
      </div>
      <div class="input-group">
        <label>암살자:</label>
        <input type="number" id="count-assassin" value="1" min="0" max="3">
      </div>
      <div class="input-group">
        <label>의사:</label>
        <input type="number" id="count-doctor" value="1" min="0" max="3">
      </div>
      <div class="input-group">
        <label>경찰:</label>
        <input type="number" id="count-police" value="1" min="0" max="3">
      </div>
      <button class="btn btn-primary" onclick="initGame()">새 게임 리셋</button>
    </div>
  </header>

  <div class="game-status-bar">
    <div>현재 단계: <span id="phase-text" class="phase-badge phase-night">밤</span></div>
    <div>일차: <span id="day-count">1</span>일차</div>
    <div>표시 생존자: <span id="alive-count">20</span> / 20명</div>
  </div>

  <div class="main-content">
    <div>
      <h3>참여 플레이어 목록 (사회자 전용 뷰)</h3>
      <br>
      <div class="grid-players" id="player-grid"></div>
    </div>

    <div class="log-container">
      <h3>진행 및 AI 토론 로그</h3>
      <div class="log-messages" id="log-box"></div>

      <div class="controls-panel">
        <button class="btn btn-warning" id="btn-night" onclick="processNight()">🌙 밤 행동 실행</button>
        <button class="btn btn-success" id="btn-discuss" onclick="processDiscussion()" disabled>🗣️ AI 토론 시작</button>
        <button class="btn btn-danger" id="btn-vote" onclick="processVote()" disabled>🗳️ 투표 진행</button>
      </div>
    </div>
  </div>

  <script>
    const TOTAL_PLAYERS = 20;
    const NAMES = [
      "탐정 셜록", "열정 시민", "냉철한 판단", "마을 이장", "동네 청년",
      "의문의 신사", "조용한 관객", "날카로운 눈", "평화주의자", "열혈 형사",
      "시골 학자", "달콤한 상인", "밤의 파수꾼", "새벽 바람", "그림자 추적",
      "지혜로운 현자", "직감 마스터", "신중한 사냥꾼", "해바라기", "하늘의 별"
    ];

    let players = [];
    let gameState = { day: 1, phase: 'NIGHT' };

    function log(msg, type = 'system') {
      const box = document.getElementById('log-box');
      const div = document.createElement('div');
      div.className = `log-item log-${type}`;
      div.innerHTML = msg;
      box.appendChild(div);
      box.scrollTop = box.scrollHeight;
    }

    function initGame() {
      const mafiaCnt = parseInt(document.getElementById('count-mafia').value);
      const assassinCnt = parseInt(document.getElementById('count-assassin').value);
      const docCnt = parseInt(document.getElementById('count-doctor').value);
      const polCnt = parseInt(document.getElementById('count-police').value);

      if (mafiaCnt + assassinCnt + docCnt + polCnt >= TOTAL_PLAYERS) {
        alert("특수 직업의 합이 전체 인원수(20명)보다 작아야 합니다.");
        return;
      }

      let roles = [];
      for(let i=0; i<mafiaCnt; i++) roles.push('마피아');
      for(let i=0; i<assassinCnt; i++) roles.push('암살자');
      for(let i=0; i<docCnt; i++) roles.push('의사');
      for(let i=0; i<polCnt; i++) roles.push('경찰');
      while(roles.length < TOTAL_PLAYERS) roles.push('시민');

      roles.sort(() => Math.random() - 0.5);

      players = Array.from({length: TOTAL_PLAYERS}, (_, i) => ({
        id: i + 1,
        name: NAMES[i],
        role: roles[i],
        isRealAlive: true,        // 실제 생존 여부
        isFakeAlive: true,        // 암살자에 의해 위장된 겉보기 생존 여부
        isRevealed: false
      }));

      gameState = { day: 1, phase: 'NIGHT' };

      document.getElementById('log-box').innerHTML = '';
      log(`🎮 게임 시작! 총 20명 (마피아 ${mafiaCnt}, 암살자 ${assassinCnt}, 의사 ${docCnt}, 경찰 ${polCnt}, 시민 ${TOTAL_PLAYERS - mafiaCnt - assassinCnt - docCnt - polCnt})`);
      log(`🌙 첫 번째 밤이 찾아왔습니다.`);

      updateUI();
    }

    function updateUI() {
      const grid = document.getElementById('player-grid');
      grid.innerHTML = '';

      let fakeAliveCount = 0;

      players.forEach(p => {
        if (p.isFakeAlive) fakeAliveCount++;
        const card = document.createElement('div');
        
        // 시각적 표시 (사회자는 위장 사망도 알 수 있도록 표시)
        const isDeadUI = !p.isFakeAlive;
        card.className = `player-card ${isDeadUI ? 'dead' : ''} ${p.isRevealed ? 'revealed' : ''}`;
        
        let roleClass = 'role-citizen';
        if (p.role === '마피아') roleClass = 'role-mafia';
        if (p.role === '암살자') roleClass = 'role-assassin';
        if (p.role === '의사') roleClass = 'role-doctor';
        if (p.role === '경찰') roleClass = 'role-police';

        let statusText = p.isRealAlive ? '생존' : (p.isFakeAlive ? '생존 (암살위장 🤫)' : '사망');
        let statusColor = p.isRealAlive ? '#4ade80' : (p.isFakeAlive ? '#c084fc' : '#f87171');

        card.innerHTML = `
          <strong>${p.name}</strong><br>
          <span class="role ${roleClass}">${p.role}</span><br>
          ${p.isRevealed ? '<span class="reveal-badge">📢 직업 공개됨</span><br>' : ''}
          <div style="font-size:0.75rem; margin-top:5px; color:${statusColor}">
            ${statusText}
          </div>
        `;
        grid.appendChild(card);
      });

      document.getElementById('alive-count').innerText = fakeAliveCount;
      document.getElementById('day-count').innerText = gameState.day;

      const phaseText = document.getElementById('phase-text');
      const btnNight = document.getElementById('btn-night');
      const btnDiscuss = document.getElementById('btn-discuss');
      const btnVote = document.getElementById('btn-vote');

      if (gameState.phase === 'NIGHT') {
        phaseText.innerText = '밤';
        phaseText.className = 'phase-badge phase-night';
        btnNight.disabled = false;
        btnDiscuss.disabled = true;
        btnVote.disabled = true;
      } else if (gameState.phase === 'DAY_DISCUSS') {
        phaseText.innerText = '낮 (토론)';
        phaseText.className = 'phase-badge phase-day';
        btnNight.disabled = true;
        btnDiscuss.disabled = false;
        btnVote.disabled = true;
      } else if (gameState.phase === 'DAY_VOTE') {
        phaseText.innerText = '낮 (투표)';
        phaseText.className = 'phase-badge phase-day';
        btnNight.disabled = true;
        btnDiscuss.disabled = true;
        btnVote.disabled = false;
      }
    }

    function processNight() {
      log(`🔒 밤 동안 능력자들이 은밀히 움직입니다...`, 'secret');

      // 1. 지난 밤 암살 위장 사망자 진짜 사망 전환
      players.forEach(p => {
        if (!p.isRealAlive && p.isFakeAlive) {
          p.isFakeAlive = false;
          log(`💀 [뒤늦은 발견] 어제 밤 암살당한 <strong>${p.name}</strong>님의 시신이 뒤늦게 발견되었습니다!`, 'system');
        }
      });

      // 2. 마피아 공격
      const mafiaTargets = players.filter(p => p.isRealAlive && p.role !== '마피아' && p.role !== '암살자');
      let mafiaKillId = null;
      if (mafiaTargets.length > 0) {
        const target = mafiaTargets[Math.floor(Math.random() * mafiaTargets.length)];
        mafiaKillId = target.id;
        log(`[비밀] 마피아가 <strong>${target.name}</strong>님을 표적으로 결정했습니다.`, 'secret');
      }

      // 3. 암살자 독자 공격 (위장 암살 능력)
      const assassin = players.find(p => p.role === '암살자' && p.isRealAlive);
      let assassinKillId = null;
      if (assassin) {
        const assTargets = players.filter(p => p.isRealAlive && p.role !== '암살자' && p.id !== mafiaKillId);
        if (assTargets.length > 0) {
          const aTarget = assTargets[Math.floor(Math.random() * assTargets.length)];
          assassinKillId = aTarget.id;
          log(`[비밀] 암살자가 <strong>${aTarget.name}</strong>님을 조용히 암살했습니다. (다음 밤 전까지 생존 위장!)`, 'secret');
        }
      }

      // 4. 의사 치료
      const doctor = players.find(p => p.role === '의사' && p.isRealAlive);
      let docSaveId = null;
      if (doctor) {
        const docTargets = players.filter(p => p.isRealAlive);
        if (docTargets.length > 0) {
          const dTarget = docTargets[Math.floor(Math.random() * docTargets.length)];
          docSaveId = dTarget.id;
          log(`[비밀] 의사가 <strong>${dTarget.name}</strong>님을 수술 치료했습니다.`, 'secret');
        }
      }

      // 5. 경찰 조사
      const police = players.find(p => p.role === '경찰' && p.isRealAlive);
      let policeRevealedPlayer = null;
      if (police) {
        const unrevealed = players.filter(p => p.isRealAlive && p.role !== '경찰' && !p.isRevealed);
        if (unrevealed.length > 0) {
          const polTarget = unrevealed[Math.floor(Math.random() * unrevealed.length)];
          polTarget.isRevealed = true;
          policeRevealedPlayer = polTarget;
          log(`[비밀] 경찰이 <strong>${polTarget.name}</strong>님을 수사했습니다.`, 'secret');
        }
      }

      log(`☀️ 날이 밝았습니다.`);

      // 결과 처리
      if (policeRevealedPlayer) {
        log(`📢 <strong>[경찰 신원 공개]</strong> <strong>${policeRevealedPlayer.name}</strong>님의 직업은 <strong>[ ${policeRevealedPlayer.role} ]</strong> 입니다!`, 'reveal');
      }

      // 마피아 공격 처리
      if (mafiaKillId && mafiaKillId !== docSaveId) {
        const deadP = players.find(p => p.id === mafiaKillId);
        deadP.isRealAlive = false;
        deadP.isFakeAlive = false;
        log(`💥 지난밤 <strong>${deadP.name}</strong>님이 습격당해 사망하셨습니다.`, 'system');
      }

      // 암살자 공격 처리 (위장 유지)
      if (assassinKillId && assassinKillId !== docSaveId) {
        const deadA = players.find(p => p.id === assassinKillId);
        deadA.isRealAlive = false;
        // isFakeAlive는 그대로 true 유지 (다음 밤전까지 로그에 안 뜸)
        log(`🤫 (암살 암시) 마을 어디선가 묘한 이질감이 느껴집니다...`, 'secret');
      }

      if (checkGameOver()) return;

      gameState.phase = 'DAY_DISCUSS';
      updateUI();
    }

    function processDiscussion() {
      // 대화는 겉보기(Fake) 생존자들이 진행
      const apparentAlive = players.filter(p => p.isFakeAlive);
      log(`🗣️ <strong>생존자들의 치열한 팩트 체크 토론이 시작됩니다.</strong>`);

      document.getElementById('btn-discuss').disabled = true;

      // 정체 드러난 악당 찾기
      const exposedEvil = players.find(p => p.isFakeAlive && p.isRevealed && (p.role === '마피아' || p.role === '암살자'));
      const talkers = [...apparentAlive].sort(() => Math.random() - 0.5).slice(0, Math.min(5, apparentAlive.length));

      let index = 0;

      const interval = setInterval(() => {
        if (index >= talkers.length) {
          clearInterval(interval);
          log(`💬 토론 종료. 지목 투표 단계로 넘어갑니다.`, 'system');
          gameState.phase = 'DAY_VOTE';
          updateUI();
          return;
        }

        const speaker = talkers[index];
        let msg = "";

        // 1. 확정 악인(마피아/암살자)이 드러난 경우: 전원이 몰아붙임
        if (exposedEvil) {
          if (speaker.id === exposedEvil.id) {
            msg = `경찰 조사는 조작입니다! 제발 저를 믿어주세요. 억울합니다!`;
          } else {
            const acc = [
              `경찰 조사로 <strong>${exposedEvil.name}</strong>님이 악당인 게 명백해졌습니다. 딴 말 필요 없이 투표하죠!`,
              `어이 <strong>${exposedEvil.name}</strong>, 발뺌해 봤자 소용없어. 투표 표 몰아줍시다.`,
              `더 이상 명분이 없네요. 이번 턴은 <strong>${exposedEvil.name}</strong>님 처형으로 확정입니다.`
            ];
            msg = acc[Math.floor(Math.random() * acc.length)];
          }
        } 
        // 2. 일반 토론 (동선 추궁 및 반박)
        else {
          const other = apparentAlive[Math.floor(Math.random() * apparentAlive.length)];
          if (speaker.role === '마피아' || speaker.role === '암살자') {
            msg = `저는 어제 내내 집 앞에 있었어요. 오히려 <strong>${other.name}</strong>님 동선이 모호하던데 해명하시죠.`;
          } else if (speaker.role === '경찰') {
            msg = `수사망을 계속 넓히고 있습니다. 섣부른 조작 발언에 현혹되지 마세요.`;
          } else {
            const cit = [
              `조용히 눈치만 보는 <strong>${other.name}</strong>님, 의심스러운데 한 마디 해보시죠?`,
              `방금 주장은 앞뒤가 안 맞잖아요. 정황상 동선이 맞는 사람부터 챙겨야 합니다.`,
              `억울한 시민이 죽지 않도록 신중하게 표를 행사합시다.`
            ];
            msg = cit[Math.floor(Math.random() * cit.length)];
          }
        }

        log(`💬 <strong>[${speaker.name}]</strong>: "${msg}"`, 'chat');
        index++;
      }, 1000);
    }

    function processVote() {
      log(`🗳️ 광장 투표 집계...`);
      const apparentAlive = players.filter(p => p.isFakeAlive);
      let votes = {};
      let invalidVotes = 0;

      const exposedEvil = players.find(p => p.isFakeAlive && p.isRevealed && (p.role === '마피아' || p.role === '암살자'));

      apparentAlive.forEach(p => {
        // 실제 사망했지만 암살 위장 상태인 플레이어는 투표 불능(무효표 처리)
        if (!p.isRealAlive && p.isFakeAlive) {
          invalidVotes++;
          return;
        }

        if (Math.random() < 0.1) { // 10% 무효표
          invalidVotes++;
        } else {
          let target = null;
          // 직업 드러난 악당이 있으면 95% 확률로 지정 투표
          if (exposedEvil && Math.random() < 0.95 && p.id !== exposedEvil.id) {
            target = exposedEvil;
          } else {
            target = apparentAlive[Math.floor(Math.random() * apparentAlive.length)];
          }
          votes[target.id] = (votes[target.id] || 0) + 1;
        }
      });

      log(`📊 <strong>투표 개봉</strong> (무효/기권/미작동 표: ${invalidVotes}표)`);

      let maxVotes = 0;
      let executedId = null;
      let isTie = false;

      for (let [id, count] of Object.entries(votes)) {
        const p = players.find(player => player.id == id);
        log(`- <strong>${p.name}</strong>: ${count}표`);
        if (count > maxVotes) {
          maxVotes = count;
          executedId = id;
          isTie = false;
        } else if (count === maxVotes) {
          isTie = true;
        }
      }

      if (isTie || !executedId) {
        log(`⚖️ 동표 또는 무효표로 처형자가 나오지 않았습니다.`, 'system');
      } else {
        const dead = players.find(p => p.id == executedId);
        dead.isRealAlive = false;
        dead.isFakeAlive = false;
        log(`⚖️ 투표 결과, 최다 표를 받은 <strong>${dead.name}</strong>님이 처형되었습니다! (정체: ${dead.role})`, 'system');
      }

      if (checkGameOver()) return;

      gameState.day++;
      gameState.phase = 'NIGHT';
      log(`🌙 다시 밤이 옵니다.`);
      updateUI();
    }

    function checkGameOver() {
      const realEvilCount = players.filter(p => p.isRealAlive && (p.role === '마피아' || p.role === '암살자')).length;
      const realGoodCount = players.filter(p => p.isRealAlive && (p.role !== '마피아' && p.role !== '암살자')).length;

      if (realEvilCount === 0) {
        log(`🎉 <strong>시민팀 승리!</strong> 모든 악당(마피아/암살자)을 소탕했습니다!`, 'system');
        disableAllButtons();
        return true;
      } else if (realEvilCount >= realGoodCount) {
        log(`☠️ <strong>악당 세력(마피아/암살자) 승리!</strong> 도시를 차지했습니다!`, 'system');
        disableAllButtons();
        return true;
      }
      return false;
    }

    function disableAllButtons() {
      document.getElementById('btn-night').disabled = true;
      document.getElementById('btn-discuss').disabled = true;
      document.getElementById('btn-vote').disabled = true;
    }

    window.onload = initGame;
  </script>
</body>
</html>
"""

components.html(html_code, height=920, scrolling=True)
