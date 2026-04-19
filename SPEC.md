<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Untold Lang — Phase 1 Syntax Spec</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; background: #ffffff; color: #111111; padding: 2rem 1.5rem; max-width: 820px; margin: 0 auto; }
  .sec-label { font-size: 11px; font-weight: 500; color: #6b7280; text-transform: uppercase; letter-spacing: .1em; margin-bottom: .6rem; padding-bottom: 6px; border-bottom: 0.5px solid #e5e7eb; }
  .section { margin-bottom: 2rem; }
  .pill-row { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 4px; }
  .pill { font-size: 12px; font-weight: 500; padding: 4px 13px; border-radius: 999px; }
  .p-purple { background: #EEEDFE; color: #3C3489; }
  .p-teal   { background: #E1F5EE; color: #085041; }
  .p-blue   { background: #E6F1FB; color: #0C447C; }
  .p-amber  { background: #FAEEDA; color: #633806; }
  .p-coral  { background: #FAECE7; color: #712B13; }
  .p-green  { background: #EAF3DE; color: #27500A; }
  .code-wrap { background: #13111E; border: 0.5px solid #2D2A42; border-radius: 10px; padding: 1rem 1.2rem; overflow-x: auto; margin-top: 4px; }
  .code-wrap pre { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: 13px; line-height: 1.85; color: #CCC8F4; white-space: pre; }
  .kw  { color: #AFA9EC; font-weight: 600; }
  .fn  { color: #5DCAA5; }
  .str { color: #EF9F27; }
  .cm  { color: #565370; }
  .ty  { color: #85B7EB; }
  .num { color: #F0997B; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 4px; }
  th { background: #534AB7; color: #fff; text-align: left; padding: 8px 12px; font-weight: 500; font-size: 12px; }
  td { padding: 7px 12px; border-bottom: 0.5px solid #e5e7eb; color: #111111; vertical-align: top; }
  tr:last-child td { border-bottom: none; }
  tr:nth-child(even) td { background: #f9fafb; }
  .mono { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: 12px; color: #534AB7; }

  @media (prefers-color-scheme: dark) {
    body { background: #0d0d0d; color: #e5e5e5; }
    .sec-label { color: #9ca3af; border-bottom-color: #2a2a2a; }
    td { color: #e5e5e5; border-bottom-color: #2a2a2a; }
    tr:nth-child(even) td { background: #1a1a1a; }
    .mono { color: #AFA9EC; }
    .p-purple { background: #3C3489; color: #CECBF6; }
    .p-teal   { background: #085041; color: #9FE1CB; }
    .p-blue   { background: #0C447C; color: #B5D4F4; }
    .p-amber  { background: #633806; color: #FAC775; }
    .p-coral  { background: #712B13; color: #F5C4B3; }
    .p-green  { background: #27500A; color: #C0DD97; }
  }
</style>
</head>
<body>

<div class="section">
  <div class="sec-label">File extension &amp; identity</div>
  <div class="pill-row">
    <span class="pill p-purple">extension: .ut</span>
    <span class="pill p-teal">paradigm: multi</span>
    <span class="pill p-blue">typing: strong + inferred</span>
    <span class="pill p-amber">style: readable &amp; expressive</span>
  </div>
</div>

<div class="section">
  <div class="sec-label">Hello world — your first .ut file</div>
  <div class="code-wrap"><pre><span class="cm">// main.ut — entry point of every Untold program</span>
<span class="kw">start</span> <span class="fn">main</span>() {
    <span class="fn">say</span>(<span class="str">"Hello, Untold World!"</span>)
}</pre></div>
</div>

<div class="section">
  <div class="sec-label">Variables &amp; types</div>
  <div class="code-wrap"><pre><span class="kw">let</span> name   = <span class="str">"Untold"</span>        <span class="cm">// inferred: text</span>
<span class="kw">let</span> version: <span class="ty">num</span>  = <span class="num">1.0</span>
<span class="kw">let</span> active : <span class="ty">bool</span> = <span class="kw">true</span>
<span class="kw">lock</span> PI    : <span class="ty">num</span>  = <span class="num">3.14159</span>   <span class="cm">// constant (immutable)</span></pre></div>
</div>

<div class="section">
  <div class="sec-label">Functions</div>
  <div class="code-wrap"><pre><span class="kw">fn</span> <span class="fn">add</span>(a: <span class="ty">num</span>, b: <span class="ty">num</span>) -> <span class="ty">num</span> {
    <span class="kw">return</span> a + b
}

<span class="cm">// Async function (for AI, web calls)</span>
<span class="kw">async fn</span> <span class="fn">fetchData</span>(url: <span class="ty">text</span>) -> <span class="ty">text</span> {
    <span class="kw">wait</span> result = <span class="fn">http.get</span>(url)
    <span class="kw">return</span> result.body
}</pre></div>
</div>

<div class="section">
  <div class="sec-label">Control flow</div>
  <div class="code-wrap"><pre><span class="kw">if</span> x > <span class="num">10</span> {
    <span class="fn">say</span>(<span class="str">"big"</span>)
} <span class="kw">elif</span> x > <span class="num">5</span> {
    <span class="fn">say</span>(<span class="str">"medium"</span>)
} <span class="kw">else</span> {
    <span class="fn">say</span>(<span class="str">"small"</span>)
}

<span class="kw">loop</span> i <span class="kw">in</span> <span class="num">0</span>..<span class="num">10</span> {         <span class="cm">// range loop</span>
    <span class="fn">say</span>(i)
}

<span class="kw">while</span> active {           <span class="cm">// while loop</span>
    <span class="fn">doWork</span>()
}</pre></div>
</div>

<div class="section">
  <div class="sec-label">Classes &amp; objects</div>
  <div class="code-wrap"><pre><span class="kw">class</span> <span class="ty">Person</span> {
    name : <span class="ty">text</span>
    age  : <span class="ty">num</span>

    <span class="kw">fn</span> <span class="fn">greet</span>() {
        <span class="fn">say</span>(<span class="str">"Hi, I am "</span> + <span class="kw">self</span>.name)
    }
}

<span class="kw">let</span> p = <span class="ty">Person</span>{ name: <span class="str">"Dev"</span>, age: <span class="num">22</span> }
p.<span class="fn">greet</span>()</pre></div>
</div>

<div class="section">
  <div class="sec-label">Modules &amp; imports</div>
  <div class="code-wrap"><pre><span class="kw">use</span> untold.ai       <span class="cm">// AI / ML module</span>
<span class="kw">use</span> untold.web      <span class="cm">// Web / HTTP module</span>
<span class="kw">use</span> untold.app      <span class="cm">// Mobile &amp; desktop UI</span>
<span class="kw">use</span> untold.net      <span class="cm">// Network &amp; sockets</span>
<span class="kw">use</span> untold.shell    <span class="cm">// Scripting &amp; system calls</span>
<span class="kw">use</span> untold.hack     <span class="cm">// Security &amp; hacking tools</span>
<span class="kw">use</span> untold.fs       <span class="cm">// File system</span>
<span class="kw">use</span> untold.db       <span class="cm">// Database access</span></pre></div>
</div>

<div class="section">
  <div class="sec-label">Error handling</div>
  <div class="code-wrap"><pre><span class="kw">try</span> {
    <span class="kw">let</span> data = <span class="fn">fs.read</span>(<span class="str">"config.ut"</span>)
} <span class="kw">catch</span> err {
    <span class="fn">say</span>(<span class="str">"Error: "</span> + err.msg)
} <span class="kw">finally</span> {
    <span class="fn">say</span>(<span class="str">"Done"</span>)
}</pre></div>
</div>

<div class="section">
  <div class="sec-label">Standard library — function signatures</div>
  <table>
    <thead><tr><th>Module</th><th>Function</th><th>Signature</th></tr></thead>
    <tbody>
      <tr><td class="mono">untold.fs</td><td class="mono">fs.read</td><td class="mono">fs.read(path: text) -&gt; text</td></tr>
      <tr><td class="mono">untold.fs</td><td class="mono">fs.write</td><td class="mono">fs.write(path: text, data: text) -&gt; void</td></tr>
      <tr><td class="mono">untold.fs</td><td class="mono">fs.exists</td><td class="mono">fs.exists(path: text) -&gt; bool</td></tr>
      <tr><td class="mono">untold.web</td><td class="mono">http.get</td><td class="mono">http.get(url: text) -&gt; Response</td></tr>
      <tr><td class="mono">untold.web</td><td class="mono">http.post</td><td class="mono">http.post(url: text, body: any) -&gt; Response</td></tr>
      <tr><td class="mono">untold.web</td><td class="mono">http.serve</td><td class="mono">http.serve(port: num) -&gt; void</td></tr>
      <tr><td class="mono">untold.ai</td><td class="mono">ai.sentiment</td><td class="mono">ai.sentiment(text: text) -&gt; SentimentResult</td></tr>
      <tr><td class="mono">untold.ai</td><td class="mono">ai.keywords</td><td class="mono">ai.keywords(text: text, n: num) -&gt; list</td></tr>
      <tr><td class="mono">untold.ai</td><td class="mono">ai.summarize</td><td class="mono">ai.summarize(text: text, n: num) -&gt; text</td></tr>
      <tr><td class="mono">untold.shell</td><td class="mono">shell.run</td><td class="mono">shell.run(cmd: text) -&gt; ShellResult</td></tr>
      <tr><td class="mono">untold.shell</td><td class="mono">shell.env</td><td class="mono">shell.env(key: text) -&gt; text</td></tr>
      <tr><td class="mono">untold.hack</td><td class="mono">hack.sha256</td><td class="mono">hack.sha256(data: text) -&gt; text</td></tr>
      <tr><td class="mono">untold.hack</td><td class="mono">hack.port_scan</td><td class="mono">hack.port_scan(host: text, s: num, e: num) -&gt; list</td></tr>
      <tr><td class="mono">untold.net</td><td class="mono">net.resolve</td><td class="mono">net.resolve(host: text) -&gt; text</td></tr>
      <tr><td class="mono">untold.net</td><td class="mono">net.my_ip</td><td class="mono">net.my_ip() -&gt; text</td></tr>
    </tbody>
  </table>
</div>

<div class="section">
  <div class="sec-label">Core keyword set</div>
  <div class="pill-row">
    <span class="pill p-purple">start</span>
    <span class="pill p-purple">fn</span>
    <span class="pill p-purple">async fn</span>
    <span class="pill p-purple">let</span>
    <span class="pill p-purple">lock</span>
    <span class="pill p-purple">class</span>
    <span class="pill p-purple">use</span>
    <span class="pill p-purple">return</span>
    <span class="pill p-purple">if / elif / else</span>
    <span class="pill p-purple">loop / while</span>
    <span class="pill p-purple">try / catch / finally</span>
    <span class="pill p-purple">wait</span>
    <span class="pill p-purple">self</span>
    <span class="pill p-purple">true / false</span>
    <span class="pill p-purple">null</span>
    <span class="pill p-purple">in</span>
    <span class="pill p-purple">break / skip</span>
  </div>
</div>

<div class="section">
  <div class="sec-label">Built-in types</div>
  <div class="pill-row">
    <span class="pill p-blue">text</span>
    <span class="pill p-blue">num</span>
    <span class="pill p-blue">bool</span>
    <span class="pill p-blue">list</span>
    <span class="pill p-blue">map</span>
    <span class="pill p-blue">void</span>
    <span class="pill p-blue">any</span>
    <span class="pill p-blue">byte</span>
    <span class="pill p-blue">func</span>
  </div>
</div>

<div class="section">
  <div class="sec-label">Domain modules</div>
  <div class="pill-row">
    <span class="pill p-teal">untold.ai</span>
    <span class="pill p-teal">untold.web</span>
    <span class="pill p-teal">untold.app</span>
    <span class="pill p-teal">untold.net</span>
    <span class="pill p-coral">untold.hack</span>
    <span class="pill p-green">untold.shell</span>
    <span class="pill p-green">untold.fs</span>
    <span class="pill p-amber">untold.db</span>
  </div>
</div>

<div class="section">
  <div class="sec-label">CLI commands</div>
  <table>
    <thead><tr><th>Command</th><th>Description</th></tr></thead>
    <tbody>
      <tr><td class="mono">untold run file.ut</td><td>Run an Untold source file</td></tr>
      <tr><td class="mono">untold new &lt;n&gt; [template]</td><td>Scaffold a new project</td></tr>
      <tr><td class="mono">untold build</td><td>Build project to executable</td></tr>
      <tr><td class="mono">untold check file.ut</td><td>Check for syntax errors</td></tr>
      <tr><td class="mono">untold install &lt;pkg&gt;</td><td>Install a package</td></tr>
      <tr><td class="mono">untold info</td><td>Show project info</td></tr>
    </tbody>
  </table>
</div>

</body>
</html>
