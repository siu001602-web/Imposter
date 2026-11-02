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
      gap: 15px;
      align-items: center;
      flex-wrap: wrap;
    }

    .input-group {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    input[type="number"] {
      width: 60px;
      padding: 6px 10px;
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
      opacity: 0.4;
      background-color: #111;
      border-color: #444;
    }

    .player-card.revealed {
      border: 2px solid #38bdf8;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
    }

    .player-card .role {
      font-size: 0.8rem;
      margin-top: 4px;
      padding: 2px 6px;
      border-radius: 4px;
      display: inline-block;
    }

    .role-mafia { background: #881337; color: #fecdd3; }
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
      height: 580px;
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
    <h1>🕵️ AI 마피아 게임 사회자 패널</h1>
    <div class="setup-panel">
      <div class="input-group">
        <label>마피아:</label>
        <input type="number" id="count-mafia" value="2" min="1" max="5">
      </div>
      <div class="input-group">
        <label>의사:</label>
        <input type="number" id="count-doctor" value="1" min="0" max="3">
      </div>
      <div class="input-group">
        <label>경찰:</label>
        <input type="number" id="count-police" value="1" min="0" max="3">
      </div>
      <button class="btn btn-primary" id="btn-reset" onclick="initGame()">새 게임 / 설정 완료</button>
    </div>
  </header>

  <div class="game-status-bar">
    <div>현재 단계: <span id="phase-text" class="phase-badge phase-night">밤</span></div>
    <div>일차: <span id="day-count">1</span>일차</div>
    <div>생존자: <span id="alive-count">20</span> / 20명</div>
  </div>

  <div class="main-content">
    <div>
      <h3>참여 플레이어 목록 (사회자 시점)</h3>
      <br>
      <div class="grid-players" id="player-grid"></div>
    </div>

    <div class="log-container">
      <h3>진행 및 실시간 대화 로그</h3>
      <div class="log-messages" id="log-box"></div>

      <div class="controls-panel">
        <button class="btn btn-warning" id="btn-night" onclick="processNight()">🌙 밤 행동 실행</button>
        <button class="btn btn-success" id="btn-discuss" onclick="processDiscussion()" disabled>🗣️ AI 실시간 토론 시작</button>
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
    let gameState = { day: 1, phase: 'NIGHT', mafiaTarget: null, doctorTarget: null, policeTarget: null };

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
      const docCnt = parseInt(document.getElementById('count-doctor').value);
      const polCnt = parseInt(document.getElementById('count-police').value);

      if (mafiaCnt + docCnt + polCnt >= TOTAL_PLAYERS) {
        alert("특수 직업의 합이 전체 인원수(20명)보다 작아야 합니다.");
        return;
      }

      let roles = [];
      for(let i=0; i<mafiaCnt; i++) roles.push('마피아');
      for(let i=0; i<docCnt; i++) roles.push('의사');
      for(let i=0; i<polCnt; i++) roles.push('경찰');
      while(roles.length < TOTAL_PLAYERS) roles.push('시민');

      roles.sort(() => Math.random() - 0.5);

      players = Array.from({length: TOTAL_PLAYERS}, (_, i) => ({
        id: i + 1,
        name: NAMES[i],
        role: roles[i],
        isAlive: true,
        isRevealed: false // 경찰 조사로 공개된 여부
      }));

      gameState = { day: 1, phase: 'NIGHT', mafiaTarget: null, doctorTarget: null, policeTarget: null };

      document.getElementById('log-box').innerHTML = '';
      log(`🎮 게임이 시작되었습니다! 총 20명 (마피아 ${mafiaCnt}, 의사 ${docCnt}, 경찰 ${polCnt}, 시민 ${TOTAL_PLAYERS - mafiaCnt - docCnt - polCnt})`);
      log(`🌙 첫 번째 밤이 시작되었습니다. [밤 행동 실행] 버튼을 눌러주세요.`);

      updateUI();
    }

    function updateUI() {
      const grid = document.getElementById('player-grid');
      grid.innerHTML = '';

      let aliveCnt = 0;
      players.forEach(p => {
        if (p.isAlive) aliveCnt++;
        const card = document.createElement('div');
        card.className = `player-card ${p.isAlive ? '' : 'dead'} ${p.isRevealed ? 'revealed' : ''}`;
        
        let roleClass = 'role-citizen';
        if (p.role === '마피아') roleClass = 'role-mafia';
        if (p.role === '의사') roleClass = 'role-doctor';
        if (p.role === '경찰') roleClass = 'role-police';

        card.innerHTML = `
          <strong>${p.name}</strong><br>
          <span class="role ${roleClass}">${p.role}</span><br>
          ${p.isRevealed ? '<span class="reveal-badge">📢 직업 공개됨</span><br>' : ''}
          <div style="font-size:0.75rem; margin-top:5px; color:${p.isAlive ? '#4ade80' : '#f87171'}">
            ${p.isAlive ? '생존' : '사망'}
          </div>
        `;
        grid.appendChild(card);
      });

      document.getElementById('alive-count').innerText = aliveCnt;
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

    function getRandomAlivePlayer(excludeRoles = []) {
      const candidates = players.filter(p => p.isAlive && !excludeRoles.includes(p.role));
      if (candidates.length === 0) return null;
      return candidates[Math.floor(Math.random() * candidates.length)];
    }

    function processNight() {
      log(`🔒 밤 동안 능력을 가진 플레이어들이 행동합니다...`, 'secret');

      // 마피아
      const mafiaTarget = getRandomAlivePlayer(['마피아']);
      gameState.mafiaTarget = mafiaTarget ? mafiaTarget.id : null;
      if (mafiaTarget) log(`[비밀] 마피아가 <strong>${mafiaTarget.name}</strong>님을 공격 표적으로 지목했습니다.`, 'secret');

      // 의사
      const doctor = players.find(p => p.role === '의사' && p.isAlive);
      if (doctor) {
        const docTarget = getRandomAlivePlayer();
        gameState.doctorTarget = docTarget ? docTarget.id : null;
        log(`[비밀] 의사가 <strong>${docTarget.name}</strong>님을 치료 대상으로 선택했습니다.`, 'secret');
      }

      // 경찰 조사 (조사 대상의 직업이 전원에게 공개됨)
      const police = players.find(p => p.role === '경찰' && p.isAlive);
      let policeRevealedPlayer = null;

      if (police) {
        // 아직 직업이 안 밝혀진 플레이어를 선호 조사
        const unrevealedCandidates = players.filter(p => p.isAlive && p.role !== '경찰' && !p.isRevealed);
        const polTarget = unrevealedCandidates.length > 0 
          ? unrevealedCandidates[Math.floor(Math.random() * unrevealedCandidates.length)]
          : getRandomAlivePlayer(['경찰']);

        if (polTarget) {
          polTarget.isRevealed = true;
          policeRevealedPlayer = polTarget;
          log(`[비밀] 경찰이 <strong>${polTarget.name}</strong>님을 조사했습니다.`, 'secret');
        }
      }

      log(`☀️ 아침이 밝았습니다.`);

      // 경찰 조사 공개 알림
      if (policeRevealedPlayer) {
        log(`📢 <strong>[경찰 조사 발표]</strong> 경찰의 조사 결과, <strong>${policeRevealedPlayer.name}</strong>님의 직업은 <strong>[ ${policeRevealedPlayer.role} ]</strong>(으)로 확인되었습니다!`, 'reveal');
      }

      // 습격 결과 처리
      if (gameState.mafiaTarget && gameState.mafiaTarget !== gameState.doctorTarget) {
        const deadPlayer = players.find(p => p.id === gameState.mafiaTarget);
        deadPlayer.isAlive = false;
        log(`💥 지난 밤, <strong>${deadPlayer.name}</strong>님이 마피아의 공격을 받아 사망하셨습니다.`, 'system');
      } else {
        log(`🛡️ 지난 밤에는 아무도 사망하지 않았습니다. (의사의 치료 성공 또는 습격 실패)`, 'system');
      }

      if (checkGameOver()) return;

      gameState.phase = 'DAY_DISCUSS';
      updateUI();
    }

    // 실시간 타이핑 형태의 토론 연출 함수
    function processDiscussion() {
      const alivePlayers = players.filter(p => p.isAlive);
      log(`🗣️ <strong>실시간 자유 토론이 시작됩니다...</strong>`);

      const btnDiscuss = document.getElementById('btn-discuss');
      btnDiscuss.disabled = true;

      // 대화 후보 5~6명 무작위 선정
      const talkers = [...alivePlayers].sort(() => Math.random() - 0.5).slice(0, Math.min(6, alivePlayers.length));
      
      let index = 0;

      const interval = setInterval(() => {
        if (index >= talkers.length) {
          clearInterval(interval);
          log(`💬 토론 시간이 종료되었습니다. 투표를 진행해 주세요.`, 'system');
          gameState.phase = 'DAY_VOTE';
          updateUI();
          return;
        }

        const p = talkers[index];
        const target = getRandomAlivePlayer();
        const revealedMafia = players.find(pl => pl.isAlive && pl.isRevealed && pl.role === '마피아');
        const revealedCitizen = players.find(pl => pl.isAlive && pl.isRevealed && pl.role !== '마피아');

        let msg = "";

        if (revealedMafia) {
          msg = `경찰 조사로 밝혀진 마피아 <strong>${revealedMafia.name}</strong>님부터 투표로 표결해야 합니다!`;
        } else if (p.role === '마피아') {
          msg = revealedCitizen 
            ? `저는 ${revealedCitizen.name}님의 신원을 믿고 시민 편에 서겠습니다. ${target.name}님이 수상해 보이네요.`
            : `저는 억울한 시민입니다! ${target.name}님의 대화 패턴이 아주 의심스럽습니다.`;
        } else if (p.role === '경찰') {
          msg = `조사 결과를 바탕으로 판세를 파악 중입니다. 성급한 투표는 자제하세요.`;
        } else if (p.role === '의사') {
          msg = `마피아의 공격에 맞서 선량한 플레이어를 보호하는 데 최선을 다하고 있습니다.`;
        } else {
          msg = `지난밤 상황과 정황상 <strong>${target.name}</strong>님에게 해명을 요구합니다.`;
        }

        log(`💬 <strong>[${p.name}]</strong>: "${msg}"`, 'chat');
        index++;
      }, 1000); // 1초 간격으로 한마디씩 실시간 출력
    }

    function processVote() {
      log(`🗳️ 최후의 투표 집계를 시작합니다...`);
      const alivePlayers = players.filter(p => p.isAlive);
      let votes = {};
      let invalidVotes = 0;

      // 공개된 마피아가 있다면 해당 플레이어에게 투표할 확률 대폭 증가
      const revealedMafia = players.find(pl => pl.isAlive && pl.isRevealed && pl.role === '마피아');

      alivePlayers.forEach(p => {
        if (Math.random() < 0.15) { // 15% 무효표
          invalidVotes++;
        } else {
          let target = null;
          if (revealedMafia && Math.random() < 0.8 && p.id !== revealedMafia.id) {
            target = revealedMafia;
          } else {
            target = alivePlayers[Math.floor(Math.random() * alivePlayers.length)];
          }
          votes[target.id] = (votes[target.id] || 0) + 1;
        }
      });

      log(`📊 <strong>투표 집계 완료</strong> (무효/기권표: ${invalidVotes}표)`);
      
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
        log(`⚖️ 동표 또는 무효표 과반으로 아무도 처형되지 않았습니다.`, 'system');
      } else {
        const dead = players.find(p => p.id == executedId);
        dead.isAlive = false;
        log(`⚖️ 투표 결과, 가장 많은 표(${maxVotes}표)를 받은 <strong>${dead.name}</strong>님이 처형되었습니다! (직업: ${dead.role})`, 'system');
      }

      if (checkGameOver()) return;

      gameState.day++;
      gameState.phase = 'NIGHT';
      log(`🌙 다시 밤이 찾아왔습니다. [밤 행동 실행]을 진행하세요.`);
      updateUI();
    }

    function checkGameOver() {
      const aliveMafia = players.filter(p => p.isAlive && p.role === '마피아').length;
      const aliveCitizen = players.filter(p => p.isAlive && p.role !== '마피아').length;

      if (aliveMafia === 0) {
        log(`🎉 <strong>시민팀 승리!</strong> 모든 마피아가 소탕되었습니다!`, 'system');
        disableAllButtons();
        return true;
      } else if (aliveMafia >= aliveCitizen) {
        log(`☠️ <strong>마피아팀 승리!</strong> 마피아가 도시를 점령했습니다!`, 'system');
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

components.html(html_code, height=900, scrolling=True)
