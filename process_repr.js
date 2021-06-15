function reprModel(model) {
    let repr = "digraph {\n";
    let codeToAct = {}
    let index = 0;
    repr += "sanode [width=\"0.75\",label=\"\",shape=\"circle\",style=filled,fillcolor=\"green\"];\n";
    repr += "eanode [width=\"0.75\",label=\"\",shape=\"circle\",style=filled,fillcolor=\"orange\"];\n";
    for (let act in model["activities_frequency"]) {
        codeToAct[act] = index;
        let label = act;
        let soj = model["sojourn_time"][act];
        label += "\nsoj="+humanizeDuration(Math.round(soj*1000));
        let actFreqCases = model["activity_frequency_cases"][act];
        let lskAnnotation = 0;
        if (act in model["lsk_annotations"]) {
            lskAnnotation = model["lsk_annotations"][act];
        }
        let tsAnnotation = 0;
        if (act in model["ts_annotations"]) {
            tsAnnotation = model["ts_annotations"][act];
        }
        label += "\n\ntc="+actFreqCases+"/cfd="+lskAnnotation+"/td="+tsAnnotation+"";
        repr += index+" [label=\""+label+"\", shape=\"box\", fontsize=\"10pt\"];\n"
        index++;
    }
    for (let it0 in model["performance_dfg"]) {
        let it = model["performance_dfg"][it0];
        let act1 = it[0][0];
        let act2 = it[0][1];
        let perf = it[1];
        let penwidth = 0.5 + Math.log10(1 + perf);
        repr += codeToAct[act1] + "->" + codeToAct[act2]+" [label=\""+humanizeDuration(Math.round(perf*1000))+"\"; penwidth=\""+penwidth+"\",fontsize=\"9pt\"];\n";
    }
    for (let sa in model["start_activities"]) {
        let count = model["start_activities"][sa];
        repr += "sanode->"+codeToAct[sa]+" [label=\"\"];\n";
    }
    for (let ea in model["end_activities"]) {
        let count = model["end_activities"][ea];
        repr += codeToAct[ea]+"->eanode [label=\"\"];\n";
    }
    repr = repr + "}\n";
    return repr;
}
