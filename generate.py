from pathlib import Path
import re
import mistune

BASE = Path(__file__).parent
md_path = BASE / 'content.md'
out_path = BASE / 'index.html'

text = md_path.read_text(encoding='utf-8')
text = text.replace('&amp;', '&')

# Split off document title block for hero use
header_split = re.split(r'\n---\s*\n', text, maxsplit=1)
header_block = header_split[0]
body_after_header = header_split[1] if len(header_split) > 1 else text

# Separate pre-week sections
intro_split = body_after_header.split('# WEEK 1:', 1)
pre_week = intro_split[0]
rest = '# WEEK 1:' + intro_split[1]

before_begin, overview_chunk = pre_week.split('# JULY CONTENT PLAN — MASTER OVERVIEW', 1)
before_begin = before_begin.strip()
overview_chunk = '# JULY CONTENT PLAN — MASTER OVERVIEW' + overview_chunk

week1, rest = rest.split('# WEEK 2:', 1)
week1 = week1.strip()
rest = '# WEEK 2:' + rest
week2, rest = rest.split('# WEEK 3:', 1)
week2 = week2.strip()
rest = '# WEEK 3:' + rest
week3, rest = rest.split('# WEEK 4:', 1)
week3 = week3.strip()
rest = '# WEEK 4:' + rest
week4, appendix = rest.split('# MAKURDI INSIGHTS', 1)
week4 = week4.strip()
appendix = '# MAKURDI INSIGHTS' + appendix

markdown = mistune.create_markdown(plugins=['table', 'strikethrough'])

before_begin_html = markdown(before_begin)
week1_html = markdown(week1)
week2_html = markdown(week2)
week3_html = markdown(week3)
week4_html = markdown(week4)
appendix_html = markdown(appendix)

# Fix heading text typo if present in source while preserving rest of content
week1_html = week1_html.replace('#FGBMI2026', '#FGBMFI2026')

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>FGBMFI 2026 Lagos National Convention — July Content Plan</title>
  <style>
    :root {{
      --sf-font: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Inter', 'Helvetica Neue', Arial, sans-serif;
      --white: #FFFFFF;
      --off-white: #FBFBFD;
      --gray-50: #F5F5F7;
      --gray-100: #E8E8ED;
      --gray-200: #D2D2D7;
      --gray-300: #AEAEB2;
      --gray-400: #86868B;
      --gray-500: #6E6E73;
      --gray-600: #48484A;
      --gray-700: #3A3A3C;
      --gray-800: #2C2C2E;
      --gray-900: #1D1D1F;
      --black: #000000;
      --blue-deep: #16213F;
      --gold: #D4AF37;
      --gold-soft: #D7BB63;
      --glass-white: rgba(255,255,255,0.72);
      --glass-white-heavy: rgba(255,255,255,0.88);
      --glass-border-subtle: rgba(0,0,0,0.06);
      --glass-shadow-sm: 0 2px 12px rgba(0,0,0,0.04);
      --glass-shadow-md: 0 8px 32px rgba(0,0,0,0.06);
      --glass-shadow-hover: 0 20px 60px rgba(0,0,0,0.10);
      --radius-sm: 12px;
      --radius-md: 16px;
      --radius-lg: 20px;
      --radius-xl: 28px;
      --radius-2xl: 36px;
      --radius-pill: 980px;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }}
    body {{ font-family: var(--sf-font); background: var(--off-white); color: var(--gray-900); line-height: 1.6; letter-spacing: -0.015em; overflow-x: hidden; font-size: 17px; }}
    ::selection {{ background: rgba(0,0,0,0.08); }}

    .bg-decoration {{ position: fixed; inset: 0; z-index: -1; background: var(--off-white); overflow: hidden; }}
    .bg-orb {{ position: absolute; border-radius: 50%; filter: blur(120px); opacity: 0.32; }}
    .bg-orb-1 {{ width: 700px; height: 700px; background: radial-gradient(circle, rgba(35,57,108,0.18), transparent 70%); top: -15%; right: -10%; animation: float1 28s ease-in-out infinite; }}
    .bg-orb-2 {{ width: 600px; height: 600px; background: radial-gradient(circle, rgba(212,175,55,0.18), transparent 70%); bottom: -10%; left: -8%; animation: float2 34s ease-in-out infinite; }}
    .bg-orb-3 {{ width: 450px; height: 450px; background: radial-gradient(circle, rgba(160,170,190,0.22), transparent 70%); top: 45%; left: 42%; animation: float3 22s ease-in-out infinite; }}
    @keyframes float1 {{ 0%,100% {{ transform: translate(0,0); }} 33% {{ transform: translate(-35px,28px); }} 66% {{ transform: translate(18px,-18px); }} }}
    @keyframes float2 {{ 0%,100% {{ transform: translate(0,0); }} 40% {{ transform: translate(28px,-22px); }} 70% {{ transform: translate(-16px,14px); }} }}
    @keyframes float3 {{ 0%,100% {{ transform: translate(0,0); }} 50% {{ transform: translate(-25px,18px); }} }}

    .scroll-progress {{ position: fixed; top: 0; left: 0; width: 0%; height: 2px; background: linear-gradient(90deg, var(--gold), var(--white)); z-index: 1002; transition: width .08s linear; }}

    .navbar {{ position: fixed; top: 0; left: 0; right: 0; z-index: 1000; padding: 0 2rem; height: 56px; display: flex; align-items: center; transition: all .4s cubic-bezier(.4,0,.2,1); }}
    .navbar.scrolled {{ background: rgba(251,251,253,0.82); backdrop-filter: saturate(180%) blur(20px); -webkit-backdrop-filter: saturate(180%) blur(20px); border-bottom: 1px solid rgba(0,0,0,0.04); }}
    .nav-container {{ max-width: 1280px; width: 100%; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; gap: 1rem; }}
    .nav-logo {{ display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--gray-900); }}
    .nav-logo-mark {{ width: 26px; height: 26px; border-radius: 8px; background: var(--gray-900); display: grid; place-items: center; }}
    .nav-logo-mark-inner {{ width: 8px; height: 8px; border-radius: 50%; background: var(--gold); }}
    .nav-logo-text {{ display: flex; flex-direction: column; line-height: 1.1; }}
    .nav-logo-name {{ font-size: .84rem; font-weight: 700; letter-spacing: -.02em; }}
    .nav-logo-sub {{ font-size: .62rem; font-weight: 500; color: var(--gray-400); }}
    .nav-links {{ display: flex; list-style: none; gap: 1.3rem; }}
    .nav-links a {{ color: var(--gray-500); text-decoration: none; font-size: .78rem; font-weight: 600; transition: color .2s ease; }}
    .nav-links a:hover {{ color: var(--gray-900); }}
    .nav-cta {{ display: inline-flex; align-items: center; gap: 8px; font-size: .77rem; font-weight: 600; color: var(--gray-900); background: var(--glass-white); border: 1px solid var(--glass-border-subtle); padding: .45rem 1rem; border-radius: var(--radius-pill); text-decoration: none; box-shadow: var(--glass-shadow-sm); transition: all .25s ease; }}
    .nav-cta:hover {{ background: var(--glass-white-heavy); box-shadow: var(--glass-shadow-md); transform: translateY(-1px); }}
    .mobile-toggle {{ display: none; background: none; border: none; color: var(--gray-900); font-size: 1.25rem; cursor: pointer; }}

    .mobile-menu {{ position: fixed; top: 0; right: -100%; width: 100%; height: 100vh; background: rgba(251,251,253,0.97); backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px); z-index: 999; padding: 5.25rem 1.5rem 2rem; transition: right .35s cubic-bezier(.4,0,.2,1); overflow-y: auto; }}
    .mobile-menu.active {{ right: 0; }}
    .mobile-nav-links {{ list-style: none; display: grid; gap: .25rem; }}
    .mobile-nav-links a {{ display: block; padding: .7rem 0; color: var(--gray-900); text-decoration: none; font-size: 1.15rem; font-weight: 650; letter-spacing: -.02em; }}

    section {{ padding: 6rem 2rem; }}
    .section-container {{ max-width: 1280px; margin: 0 auto; }}
    .section-label {{ display: inline-flex; align-items: center; gap: 8px; font-size: .67rem; font-weight: 700; color: var(--gray-400); text-transform: uppercase; letter-spacing: .1em; margin-bottom: .9rem; }}
    .section-title {{ font-size: clamp(2rem, 4vw, 3.2rem); font-weight: 740; line-height: 1.05; letter-spacing: -.045em; color: var(--gray-900); margin-bottom: .8rem; }}
    .section-subtitle {{ font-size: 1rem; color: var(--gray-500); line-height: 1.72; max-width: 760px; }}
    .section-header-centered {{ text-align: center; margin-bottom: 3rem; }}
    .section-header-centered .section-subtitle {{ margin: 0 auto; }}
    .section-divider {{ max-width: 1280px; margin: 0 auto; height: 1px; background: var(--gray-100); }}

    .hero {{ min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 8rem 2rem 5rem; text-align: center; background: linear-gradient(180deg, #111827 0%, #111318 100%); position: relative; overflow: hidden; }}
    .hero::before {{ content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 34%, rgba(212,175,55,.12) 0%, transparent 60%); pointer-events: none; }}
    .hero-content {{ max-width: 980px; position: relative; z-index: 1; }}
    .hero-badge {{ display: inline-flex; align-items: center; gap: 8px; padding: 7px 16px; background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.14); border-radius: var(--radius-pill); font-size: .72rem; font-weight: 700; color: rgba(255,255,255,.62); margin-bottom: 1.35rem; text-transform: uppercase; letter-spacing: .08em; }}
    .hero-dot {{ width: 6px; height: 6px; border-radius: 50%; background: var(--gold); }}
    .hero-kicker {{ display: block; font-size: .74rem; color: rgba(255,255,255,.4); text-transform: uppercase; letter-spacing: .12em; font-weight: 700; margin-bottom: 1.1rem; }}
    .hero h1 {{ font-size: clamp(2.6rem, 6vw, 5rem); font-weight: 760; line-height: 1.02; letter-spacing: -.05em; color: var(--white); margin-bottom: .9rem; }}
    .hero-theme {{ font-size: clamp(.98rem, 2vw, 1.18rem); color: rgba(255,255,255,.55); font-style: italic; margin-bottom: 1.25rem; }}
    .hero-subtitle {{ font-size: clamp(.96rem, 1.7vw, 1.08rem); color: rgba(255,255,255,.58); line-height: 1.76; max-width: 720px; margin: 0 auto 2rem; }}
    .hero-buttons {{ display: flex; justify-content: center; flex-wrap: wrap; gap: .85rem; }}
    .btn-dark, .btn-glass {{ display: inline-flex; align-items: center; gap: 8px; padding: .9rem 1.55rem; border-radius: var(--radius-pill); text-decoration: none; font-size: .92rem; font-weight: 600; letter-spacing: -.01em; transition: all .25s ease; }}
    .btn-dark {{ background: var(--white); color: var(--gray-900); box-shadow: 0 12px 32px rgba(0,0,0,.18); }}
    .btn-dark:hover {{ transform: translateY(-2px); box-shadow: 0 20px 44px rgba(0,0,0,.22); }}
    .btn-glass {{ background: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.12); color: rgba(255,255,255,.88); }}
    .btn-glass:hover {{ background: rgba(255,255,255,.13); transform: translateY(-2px); }}
    .hero-meta {{ display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 1rem; margin-top: 4rem; padding-top: 2.2rem; border-top: 1px solid rgba(255,255,255,.08); }}
    .meta-item {{ text-align: center; }}
    .meta-label {{ font-size: .66rem; color: rgba(255,255,255,.33); text-transform: uppercase; letter-spacing: .09em; font-weight: 700; margin-bottom: 6px; }}
    .meta-value {{ font-size: .95rem; color: rgba(255,255,255,.82); font-weight: 650; letter-spacing: -.02em; }}

    .glass-card, .glass-card-flat {{ background: var(--glass-white-heavy); backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px); border: 1px solid var(--glass-border-subtle); border-radius: var(--radius-xl); box-shadow: var(--glass-shadow-sm); position: relative; overflow: hidden; }}
    .glass-card::before, .glass-card-flat::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,.9), transparent); pointer-events: none; }}
    .glass-card {{ transition: all .35s cubic-bezier(.4,0,.2,1); }}
    .glass-card:hover {{ transform: translateY(-3px); box-shadow: var(--glass-shadow-hover); border-color: rgba(0,0,0,.07); }}

    .cards-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 1.1rem; }}
    .card-pad {{ padding: 2rem; }}
    .mini-label {{ display: inline-flex; align-items: center; gap: 8px; padding: 5px 12px; border-radius: var(--radius-pill); background: var(--gray-900); color: var(--white); font-size: .64rem; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; margin-bottom: 1rem; }}
    .card-title {{ font-size: 1.05rem; font-weight: 720; letter-spacing: -.025em; color: var(--gray-900); margin-bottom: .55rem; }}
    .card-body {{ color: var(--gray-600); font-size: .9rem; line-height: 1.7; }}
    .quote-band {{ margin-top: 1.1rem; padding: 1.25rem 1.4rem; border-radius: var(--radius-lg); background: rgba(17,24,39,.98); color: rgba(255,255,255,.76); }}
    .quote-band strong {{ color: var(--white); }}

    .week-grid {{ display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 2px; background: var(--gray-100); border-radius: var(--radius-xl); overflow: hidden; }}
    .week-grid .glass-card-flat {{ border-radius: 0; box-shadow: none; border: 0; }}
    .week-card {{ padding: 2rem 1.5rem; min-height: 230px; }}
    .week-num {{ font-size: .62rem; font-weight: 700; color: var(--gray-400); text-transform: uppercase; letter-spacing: .08em; margin-bottom: .6rem; }}
    .week-name {{ font-size: 1rem; font-weight: 720; color: var(--gray-900); letter-spacing: -.03em; margin-bottom: .45rem; }}
    .week-period {{ font-size: .74rem; font-weight: 650; color: var(--gray-400); margin-bottom: .95rem; }}
    .week-desc {{ font-size: .85rem; color: var(--gray-500); line-height: 1.62; }}

    .table-card {{ padding: 0; overflow: hidden; }}
    .table-wrap {{ overflow-x: auto; }}
    table {{ width: 100%; border-collapse: collapse; min-width: 760px; }}
    th {{ padding: .9rem 1.15rem; text-align: left; font-size: .66rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--gray-400); background: var(--gray-50); border-bottom: 1px solid rgba(0,0,0,.05); }}
    td {{ padding: .95rem 1.15rem; color: var(--gray-600); font-size: .87rem; line-height: 1.55; border-bottom: 1px solid rgba(0,0,0,.04); vertical-align: top; }}
    tr:last-child td {{ border-bottom: 0; }}
    td strong {{ color: var(--gray-900); }}

    .tabs-shell {{ margin-top: 3rem; }}
    .tab-nav {{ display: flex; gap: .45rem; justify-content: center; flex-wrap: wrap; padding: 5px; background: var(--glass-white); border: 1px solid var(--glass-border-subtle); border-radius: var(--radius-pill); box-shadow: var(--glass-shadow-sm); width: max-content; max-width: 100%; margin: 0 auto 2rem; }}
    .tab-btn {{ appearance: none; border: 0; background: transparent; padding: .6rem 1.15rem; border-radius: var(--radius-pill); font-size: .8rem; font-weight: 650; color: var(--gray-500); cursor: pointer; transition: all .25s ease; font-family: inherit; }}
    .tab-btn:hover {{ color: var(--gray-900); }}
    .tab-btn.active {{ background: var(--gray-900); color: var(--white); }}
    .tab-pane {{ display: none; }}
    .tab-pane.active {{ display: block; animation: tabFade .35s ease; }}
    @keyframes tabFade {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}

    .pane-note {{ margin-bottom: 1rem; padding: 1rem 1.1rem; border-radius: var(--radius-lg); background: rgba(17,24,39,.96); color: rgba(255,255,255,.72); font-size: .88rem; line-height: 1.7; }}

    .prose-wrap {{ padding: 2rem 2rem 2.2rem; }}
    .prose {{ color: var(--gray-700); }}
    .prose > *:first-child {{ margin-top: 0 !important; }}
    .prose h1, .prose h2, .prose h3, .prose h4 {{ color: var(--gray-900); letter-spacing: -.03em; line-height: 1.15; }}
    .prose h1 {{ font-size: clamp(1.7rem, 3vw, 2.55rem); font-weight: 760; margin: 0 0 1rem; }}
    .prose h2 {{ font-size: clamp(1.35rem, 2.4vw, 2rem); font-weight: 740; margin: 2rem 0 .8rem; }}
    .prose h3 {{ font-size: 1.08rem; font-weight: 720; margin: 1.45rem 0 .6rem; }}
    .prose h4 {{ font-size: .95rem; font-weight: 700; margin: 1.1rem 0 .4rem; text-transform: uppercase; color: var(--gray-500); letter-spacing: .06em; }}
    .prose p {{ margin: .7rem 0; line-height: 1.8; color: var(--gray-600); }}
    .prose em {{ color: var(--gray-500); }}
    .prose strong {{ color: var(--gray-900); }}
    .prose ul, .prose ol {{ margin: .65rem 0 1rem 1.2rem; color: var(--gray-600); }}
    .prose li {{ margin: .28rem 0; line-height: 1.72; }}
    .prose hr {{ margin: 1.6rem 0; border: 0; height: 1px; background: var(--gray-100); }}
    .prose pre {{ margin: .75rem 0 1.1rem; padding: 1rem 1rem 1.05rem; border-radius: 18px; background: #111827; color: rgba(255,255,255,.88); overflow-x: auto; border: 1px solid rgba(255,255,255,.06); box-shadow: inset 0 1px 0 rgba(255,255,255,.04); }}
    .prose pre code {{ white-space: pre-wrap; word-break: break-word; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: .84rem; line-height: 1.72; display: block; }}
    .prose code {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }}
    .prose table {{ width: 100%; min-width: 680px; margin: 1rem 0 1.3rem; border-collapse: collapse; }}
    .prose thead th {{ background: var(--gray-900); color: rgba(255,255,255,.74); }}
    .prose tbody tr:nth-child(even) td {{ background: rgba(0,0,0,.012); }}
    .prose blockquote {{ margin: 1rem 0; padding: 1rem 1.1rem; border-left: 3px solid var(--gold); background: rgba(212,175,55,.08); border-radius: 0 var(--radius-md) var(--radius-md) 0; color: var(--gray-700); }}

    .closing-section {{ background: var(--gray-900); padding: 8rem 2rem; text-align: center; }}
    .closing-inner {{ max-width: 780px; margin: 0 auto; }}
    .closing-eyebrow {{ display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px; background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.1); border-radius: var(--radius-pill); font-size: .68rem; font-weight: 700; color: rgba(255,255,255,.38); text-transform: uppercase; letter-spacing: .08em; margin-bottom: 1.6rem; }}
    .closing-title {{ font-size: clamp(2rem, 5vw, 3.7rem); font-weight: 760; line-height: 1.05; letter-spacing: -.05em; color: var(--white); margin-bottom: 1rem; }}
    .closing-body {{ color: rgba(255,255,255,.55); font-size: 1rem; line-height: 1.8; margin-bottom: 2rem; }}
    .prepared-card {{ padding: 2rem; background: rgba(255,255,255,.04); border: 1px solid rgba(255,255,255,.08); border-radius: var(--radius-xl); text-align: left; }}
    .prepared-label {{ font-size: .64rem; font-weight: 700; color: rgba(255,255,255,.32); text-transform: uppercase; letter-spacing: .1em; margin-bottom: .9rem; }}
    .prepared-org {{ font-size: 1.08rem; font-weight: 730; color: var(--white); margin-bottom: .2rem; }}
    .prepared-desc {{ font-size: .82rem; color: rgba(255,255,255,.45); margin-bottom: 1rem; }}
    .prepared-divider {{ height: 1px; background: rgba(255,255,255,.08); margin-bottom: 1rem; }}
    .prepared-client {{ font-size: .84rem; color: rgba(255,255,255,.52); line-height: 1.7; }}
    .prepared-client strong {{ color: rgba(255,255,255,.78); }}

    .footer {{ background: var(--gray-900); padding: 1.8rem 2rem; border-top: 1px solid rgba(255,255,255,.05); }}
    .footer-inner {{ max-width: 1280px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; gap: 1rem; flex-wrap: wrap; }}
    .footer-brand {{ display: flex; align-items: center; gap: 8px; }}
    .footer-mark {{ width: 20px; height: 20px; border-radius: 6px; background: rgba(255,255,255,.1); display: grid; place-items: center; }}
    .footer-mark span {{ width: 6px; height: 6px; border-radius: 50%; background: rgba(255,255,255,.4); }}
    .footer-brand-name {{ color: rgba(255,255,255,.34); font-size: .78rem; font-weight: 600; }}
    .footer-note {{ color: rgba(255,255,255,.24); font-size: .72rem; }}

    .reveal {{ opacity: 0; transform: translateY(26px); transition: all .75s cubic-bezier(.4,0,.2,1); }}
    .reveal.active {{ opacity: 1; transform: translateY(0); }}

    @media (max-width: 1100px) {{
      .nav-links, .nav-cta {{ display: none; }}
      .mobile-toggle {{ display: inline-flex; }}
      .cards-grid {{ grid-template-columns: repeat(2, minmax(0,1fr)); }}
      .week-grid {{ grid-template-columns: repeat(2, minmax(0,1fr)); }}
      .hero-meta {{ grid-template-columns: repeat(2, minmax(0,1fr)); }}
    }}
    @media (max-width: 768px) {{
      section {{ padding: 4rem 1.25rem; }}
      .hero {{ padding: 7rem 1.25rem 4rem; }}
      .hero-buttons {{ flex-direction: column; align-items: center; }}
      .hero-meta {{ grid-template-columns: 1fr; gap: 1.2rem; }}
      .cards-grid, .week-grid {{ grid-template-columns: 1fr; }}
      .prose-wrap {{ padding: 1.4rem 1.1rem 1.6rem; }}
      .footer-inner {{ flex-direction: column; text-align: center; }}
    }}
    @media (max-width: 480px) {{ body {{ font-size: 16px; }} }}
  </style>
</head>
<body>
  <div class="bg-decoration">
    <div class="bg-orb bg-orb-1"></div>
    <div class="bg-orb bg-orb-2"></div>
    <div class="bg-orb bg-orb-3"></div>
  </div>

  <div class="scroll-progress" id="scrollProgress"></div>

  <nav class="navbar" id="navbar">
    <div class="nav-container">
      <a class="nav-logo" href="#home">
        <div class="nav-logo-mark"><div class="nav-logo-mark-inner"></div></div>
        <div class="nav-logo-text">
          <span class="nav-logo-name">Shutter Space</span>
          <span class="nav-logo-sub">FGBMFI July 2026 Copy Deck</span>
        </div>
      </a>
      <ul class="nav-links">
        <li><a href="#strategy">Strategy</a></li>
        <li><a href="#overview">Overview</a></li>
        <li><a href="#database">Database</a></li>
        <li><a href="#appendix">Tracker</a></li>
      </ul>
      <a class="nav-cta" href="#database">Open Copy Database</a>
      <button class="mobile-toggle" id="mobileToggle" aria-label="Menu">☰</button>
    </div>
  </nav>

  <div class="mobile-menu" id="mobileMenu">
    <ul class="mobile-nav-links">
      <li><a href="#strategy">Strategy</a></li>
      <li><a href="#overview">Overview</a></li>
      <li><a href="#database">Content Database</a></li>
      <li><a href="#appendix">Makurdi Tracker</a></li>
      <li><a href="#closing">Closing</a></li>
    </ul>
  </div>

  <section class="hero" id="home">
    <div class="hero-content">
      <div class="hero-badge reveal active"><span class="hero-dot"></span> Full Copy Database · July 2026</div>
      <span class="hero-kicker">FGBMFI Nigeria · Lagos National Convention 2026</span>
      <h1>31 Days.<br/>All Platforms.<br/>One July Engine.</h1>
      <p class="hero-theme">“Pressing Toward The Mark” · November 11–14, 2026 · National Arts Theatre, Lagos</p>
      <p class="hero-subtitle">
        A long-form campaign webpage built in the saved Shutter Space layout system — housing the complete July content plan, week-by-week roll-out, platform copy, speaker reveals, Makurdi insight deployment, and final scheduling notes for review.
      </p>
      <div class="hero-buttons">
        <a class="btn-dark" href="#database">Open Content Database</a>
        <a class="btn-glass" href="#appendix">View Insight Tracker</a>
      </div>
      <div class="hero-meta">
        <div class="meta-item"><div class="meta-label">Campaign Span</div><div class="meta-value">31 Days</div></div>
        <div class="meta-item"><div class="meta-label">Weekly Themes</div><div class="meta-value">4 Distinct Weeks</div></div>
        <div class="meta-item"><div class="meta-label">Platform Set</div><div class="meta-value">Instagram · Facebook · TikTok · LinkedIn · X</div></div>
        <div class="meta-item"><div class="meta-label">Source Engine</div><div class="meta-value">40 Makurdi Insights</div></div>
      </div>
    </div>
  </section>

  <div class="section-divider"></div>

  <section id="strategy">
    <div class="section-container">
      <div class="section-header-centered reveal">
        <span class="section-label">⚙️ Before We Begin</span>
        <h2 class="section-title">How the Makurdi<br/>Insights Are Working</h2>
        <p class="section-subtitle">The 2025 Makurdi Regional Convention teachings are the intellectual engine behind the July plan — reused as hooks, quote cards, educational carousels, depth signals, and youth-facing relevance drivers.</p>
      </div>
      <div class="cards-grid">
        <div class="glass-card card-pad reveal">
          <div class="mini-label">Use 01</div>
          <div class="card-title">Quote Graphics</div>
          <p class="card-body">Short, premium visual cards turn single teachings into high-share social assets that can circulate across Instagram, Facebook, X, and WhatsApp without heavy production overhead.</p>
        </div>
        <div class="glass-card card-pad reveal">
          <div class="mini-label">Use 02</div>
          <div class="card-title">Reels & TikTok Hooks</div>
          <p class="card-body">Insights become talk-to-camera openings like “Are you a thermostat or a thermometer in your business?” — giving the content immediate tension and relevance.</p>
        </div>
        <div class="glass-card card-pad reveal">
          <div class="mini-label">Use 03</div>
          <div class="card-title">Caption Themes</div>
          <p class="card-body">Each teaching anchors the body of a post, making the campaign feel deep, coherent, and spiritually intelligent rather than hype-driven or repetitive.</p>
        </div>
        <div class="glass-card card-pad reveal">
          <div class="mini-label">Use 04</div>
          <div class="card-title">Carousel Education</div>
          <p class="card-body">Multi-slide explainers translate convention teachings into digestible, platform-native learning assets — especially useful for marketplace and theme content.</p>
        </div>
        <div class="glass-card card-pad reveal">
          <div class="mini-label">Use 05</div>
          <div class="card-title">Credibility & Depth</div>
          <p class="card-body">The insights prove FGBMFI produces real, substantive content. They answer skepticism by showing thought, theology, discipline, and marketplace intelligence.</p>
        </div>
        <div class="glass-card card-pad reveal">
          <div class="mini-label">Use 06</div>
          <div class="card-title">Young Audience Relevance</div>
          <p class="card-body">They help answer the core youth question: <strong>“Why should I attend this?”</strong> — by connecting the fellowship directly to ambition, identity, work, leadership, and purpose.</p>
        </div>
      </div>
      <div class="glass-card-flat card-pad reveal" style="margin-top: 1.1rem;">
        <div class="prose">{before_begin_html}</div>
      </div>
      <div class="quote-band reveal">
        <strong>The framing:</strong> “This is what happened at one of our regional conventions last year. Imagine what the National Convention in Lagos is going to produce.”
      </div>
    </div>
  </section>

  <div class="section-divider"></div>

  <section id="overview">
    <div class="section-container">
      <div class="section-header-centered reveal">
        <span class="section-label">🗓️ July Architecture</span>
        <h2 class="section-title">The Month at a Glance</h2>
        <p class="section-subtitle">Four themed weeks. Five core platforms. One coordinated campaign rhythm designed to announce, deepen, prove, mobilize, and convert.</p>
      </div>

      <div class="week-grid reveal">
        <div class="glass-card-flat week-card">
          <div class="week-num">Week 1</div>
          <div class="week-name">The Grand Launch</div>
          <div class="week-period">July 1–7</div>
          <p class="week-desc">Announce the event, launch the visual world, drop the trailer, establish new platforms, and begin speaker reveals with maximum signal.</p>
        </div>
        <div class="glass-card-flat week-card">
          <div class="week-num">Week 2</div>
          <div class="week-name">Speakers + Substance</div>
          <div class="week-period">July 8–14</div>
          <p class="week-desc">Continue high-value speaker reveals while deploying Makurdi insights to prove the convention carries real marketplace and spiritual depth.</p>
        </div>
        <div class="glass-card-flat week-card">
          <div class="week-num">Week 3</div>
          <div class="week-name">Programmes + Proof</div>
          <div class="week-period">July 15–21</div>
          <p class="week-desc">Show how the event actually serves professionals, share testimonies, and make the case especially clear for younger attendees.</p>
        </div>
        <div class="glass-card-flat week-card">
          <div class="week-num">Week 4</div>
          <div class="week-name">Community + Momentum</div>
          <div class="week-period">July 22–31</div>
          <p class="week-desc">Push chapter mobilization, social proof, challenge participation, registration momentum, and the transition into an even bigger August.</p>
        </div>
      </div>

      <div class="glass-card-flat table-card reveal" style="margin-top: 1.1rem;">
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Platform</th>
                <th>Feed / Posts</th>
                <th>Stories</th>
                <th>Reels / TikToks</th>
                <th>Lives</th>
              </tr>
            </thead>
            <tbody>
              <tr><td><strong>Instagram</strong></td><td>Daily</td><td>Daily (5–7 slides)</td><td>4–5x per week</td><td>None in July</td></tr>
              <tr><td><strong>Facebook</strong></td><td>Daily</td><td>N/A</td><td>3x per week</td><td>1 at end of month</td></tr>
              <tr><td><strong>TikTok</strong></td><td>Daily</td><td>N/A</td><td>Daily</td><td>None</td></tr>
              <tr><td><strong>LinkedIn</strong></td><td>4x per week</td><td>N/A</td><td>2x per week</td><td>None</td></tr>
              <tr><td><strong>X (Twitter)</strong></td><td>3–5x daily</td><td>N/A</td><td>N/A</td><td>None</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </section>

  <div class="section-divider"></div>

  <section id="database">
    <div class="section-container">
      <div class="section-header-centered reveal">
        <span class="section-label">📚 Full Copy Database</span>
        <h2 class="section-title">Every Week.<br/>Every Day. Every Copy Block.</h2>
        <p class="section-subtitle">The content below preserves the full working copy structure: captions, visual briefs, story slides, scripts, tweets, speaker reveals, testimonial language, programme explainers, and community prompts.</p>
      </div>

      <div class="tabs-shell reveal">
        <div class="tab-nav" role="tablist" aria-label="Weekly content plan tabs">
          <button class="tab-btn active" data-tab="week1">Week 1</button>
          <button class="tab-btn" data-tab="week2">Week 2</button>
          <button class="tab-btn" data-tab="week3">Week 3</button>
          <button class="tab-btn" data-tab="week4">Week 4</button>
          <button class="tab-btn" data-tab="appendix-tab">Appendix</button>
        </div>

        <div class="tab-pane active" id="week1">
          <div class="pane-note">Launch week: official announcement, trailer release, first major speaker reveals, theme framing, Sunday faith content, and a “What is FGBMFI?” explainer for new audiences.</div>
          <div class="glass-card-flat prose-wrap"><article class="prose">{week1_html}</article></div>
        </div>

        <div class="tab-pane" id="week2">
          <div class="pane-note">Depth week: speaker continuity meets Makurdi insight deployment — thermostat leadership, integrity in business, legacy, professional gates, challenge launch, and venue framing.</div>
          <div class="glass-card-flat prose-wrap"><article class="prose">{week2_html}</article></div>
        </div>

        <div class="tab-pane" id="week3">
          <div class="pane-note">Proof week: programmes, testimonials, younger audience messaging, governance credibility, fellowship education, and reason-to-attend content that bridges generations.</div>
          <div class="glass-card-flat prose-wrap"><article class="prose">{week3_html}</article></div>
        </div>

        <div class="tab-pane" id="week4">
          <div class="pane-note">Momentum week: chapter mobilization, national representation, registration proof, prayer, testimony, speaker wrap-ups, and the bridge into August.</div>
          <div class="glass-card-flat prose-wrap"><article class="prose">{week4_html}</article></div>
        </div>

        <div class="tab-pane" id="appendix-tab">
          <div class="pane-note" id="appendix">Appendix: full Makurdi insights deployment tracker, X daily tweet schedule, and final document closeout notes.</div>
          <div class="glass-card-flat prose-wrap"><article class="prose">{appendix_html}</article></div>
        </div>
      </div>
    </div>
  </section>

  <section class="closing-section" id="closing">
    <div class="closing-inner">
      <div class="closing-eyebrow">Prepared & Packaged</div>
      <h2 class="closing-title">Ready for review,<br/>design briefing, and scheduling.</h2>
      <p class="closing-body">This page translates the saved Shutter Space layout preset into a working content-deck webpage for the FGBMFI Lagos 2026 July campaign. It is optimized as a review document, a planning reference, and a design handoff surface.</p>
      <div class="prepared-card">
        <div class="prepared-label">Document Credits</div>
        <div class="prepared-org">FGBMFI 2026 Lagos National Convention — Complete July Content Plan</div>
        <div class="prepared-desc">Full copy database · Version 2.0 · Built in the Shutter Space editorial glass layout system</div>
        <div class="prepared-divider"></div>
        <div class="prepared-client">
          <strong>Prepared by:</strong> Jecoliah<br/>
          <strong>For Review:</strong> Pelumi | Shutter Space<br/>
          <strong>Client:</strong> FGBMFI Nigeria<br/>
          <strong>Event:</strong> 2026 Lagos National Convention — “Pressing Toward The Mark”<br/>
          <strong>Dates:</strong> November 11–14, 2026 · National Arts Theatre, Lagos<br/>
          <strong>Next Deliverable:</strong> August Content Plan
        </div>
      </div>
    </div>
  </section>

  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <div class="footer-mark"><span></span></div>
        <div class="footer-brand-name">Shutter Space Layout System</div>
      </div>
      <div class="footer-note">Standalone HTML · Inline styles · No external dependencies</div>
    </div>
  </footer>

  <script>
    const navbar = document.getElementById('navbar');
    const progress = document.getElementById('scrollProgress');
    const mobileToggle = document.getElementById('mobileToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    const reveals = document.querySelectorAll('.reveal');

    function onScroll() {{
      const scrolled = window.scrollY > 18;
      navbar.classList.toggle('scrolled', scrolled);
      const max = document.documentElement.scrollHeight - window.innerHeight;
      const pct = max > 0 ? (window.scrollY / max) * 100 : 0;
      progress.style.width = pct + '%';
    }}

    function revealOnScroll() {{
      const trigger = window.innerHeight * 0.9;
      reveals.forEach(el => {{
        const top = el.getBoundingClientRect().top;
        if (top < trigger) el.classList.add('active');
      }});
    }}

    mobileToggle.addEventListener('click', () => {{
      mobileMenu.classList.toggle('active');
    }});

    mobileMenu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {{
      mobileMenu.classList.remove('active');
    }}));

    tabButtons.forEach(btn => {{
      btn.addEventListener('click', () => {{
        const target = btn.dataset.tab;
        tabButtons.forEach(b => b.classList.remove('active'));
        tabPanes.forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(target).classList.add('active');
        window.scrollTo({{ top: document.getElementById('database').offsetTop - 70, behavior: 'smooth' }});
      }});
    }});

    window.addEventListener('scroll', () => {{ onScroll(); revealOnScroll(); }});
    window.addEventListener('load', () => {{ onScroll(); revealOnScroll(); }});
  </script>
</body>
</html>
'''

out_path.write_text(html, encoding='utf-8')
print(f'Wrote {out_path}')
