
{% for chart in charts %}
	<div id="{{forloop.counter}}" hidden>
	{{ chart.as_html }}
	</div>
{% endfor %}
<button id="next" onclick="next();">Next</button>

<script type="text/javascript">
	var visible = 1;
	var total = Number({{chart.length}});
	document.getElementById(visible.toString()).removeAttribute("hidden");
	function next(e) {
		// body...
		document.getElementById(visible.toString()).setAttribute("hidden", "hidden");
		visible = (1+visible)%total;
		document.getElementById(visible.toString()).removeAttribute("hidden");
	}
</script>
