function create(mode) {
    var main_element = document.getElementById("quiz");
    context = [
        ["問題：請想想寶特瓶除了裝飲料，還有哪些功能？請使用滑鼠點選數字編號右側底線處，並依序輸入你想到的答案(1、2、3...)，請使用五個字以內簡要的詞彙描述。", "註：寶特瓶的尺寸跟我們平常使用的差不多，你可以同時使用很多個寶特瓶。"],
        ["問題：請想想吸管除了喝飲料，還有哪些功能？請使用滑鼠點選數字編號右側底線處，並依序輸入你想到的答案(1、2、3...)，請使用五個字以內簡要的詞彙描述。", "註：吸管的尺寸跟我們平常使用的差不多，你可以同時使用很多根吸管。"],
        ["問題：請想想竹筷子除了吃飯夾菜夾肉，還有哪些功能？請使用滑鼠點選數字編號右側底線處，並依序輸入你想到的答案(1、2、3...)，請使用五個字以內簡要的詞彙描述。", "註：竹筷子的尺寸跟我們平常使用的差不多，你可以同時使用很多根竹筷子。"],
        ["請你試著找出一個「答案字」，使得該「答案字」可以與前面三個「線索字」各自組合成為另外一個常見的合法中文字。", "請使用滑鼠點選題目右側底線處，並輸入你想到的答案(作答順序不限制)。"],
        ["請你試著找出一個「答案字」，使得該「答案字」可以與前面三個「線索字」各自組合成為另外一個常見的合法中文字。", "請使用滑鼠點選題目右側底線處，並輸入你想到的答案(作答順序不限制)。"],
        ["請你試著找出一個「答案字」，使得該「答案字」可以與前面三個「線索字」各自組合成為另外一個常見的<b>中文雙字詞</b>。", "請使用滑鼠點選題目右側底線處，並輸入你想到的答案(作答順序不限制)。"]
    ]

    quizText = [
        ["爭、日、米", "交、甫、兩", "考、登、乍", "羔、唐、量", "夕、八、木", "重、奴、工", "平、青、吳", "考、登、乍", "云、令、而", "工、且、重", "相、今、亡", "且、呈、責", "二、哥、區", "屯、令、予", "炎、射、周", "口、言、兄", "口、爪、父", "宛、馬、楚", "言、爭、日", "午、十、寸"],
        ["川、火、豆", "乍、勿、能", "工、牙、躬", "司、式、寺", "口、田、奴", "乃、古、夷", "皮、並、茲", "忍、吾、斥", "淮、曰、言", "俞、專、甫", "支、寸、目", "良、昏、馬", "口、才、次", "果、敬、宜", "貝、昌、卑", "日、券、其", "兄、口、淮", "日、米、言", "禾、矢、力", "雇、彥、原"],
        ["原、迷、想", "擊、藥、斷", "存、女、寫", "交、異、別", "案、官、書", "所、景、職", "落、沉、命", "代、童、級", "考、產、測", "得、逃、過", "建、新、趣", "專、遠、官", "整、步、度", "領、首、求 ", "員、計、體", "當、宜、輕", "數、女、減 ", "通、業、李", "展、改、度", "暴、營、透"]
    ]
    quizmode = parseInt(mode / 10);
    quizNumber = parseInt(mode) % 10;
    userid = getCookie("userid");
    MN = parseInt(userid % 2);

    main_element.innerHTML = "<div id='title'>" + context[quizNumber][0] + "</div><br> <div id='describe'>" + context[quizNumber][1] + "</div><br>";
    var _ment = document.createElement("div");
    _ment.setAttribute("class", "row");
    _ment.setAttribute("style", "width:1200px;");
    for (var i = 0; i < quizmode + 1; i++) {
        var _ent = document.createElement("div");
        if (quizmode) {
            _ent.setAttribute("class", "col-5");
        } else {
            _ent.setAttribute("class", "col");
        }

        _ent.setAttribute("style", "text-align:center;");
        _ent.innerHTML = "<b>" + "Player " + String(parseInt(i ? (userid % 2 ? parseInt(userid) - 1 : parseInt(userid) + 1) : userid)) + "</b>";
        _ment.appendChild(_ent);
        _ent = document.createElement("div");
        _ent.setAttribute("class", "col-1");
        _ment.appendChild(_ent);
    }
    main_element.appendChild(_ment);

    for (var i = 0; i < (quizNumber >= 3 ? 10 : 15); i++) {
        var _element = document.createElement("div");
        _element.setAttribute("class", "row");
        _element.setAttribute("style", "width:1200px;");
        _element.setAttribute("id", "box");

        for (var k = 0; k < (quizmode + 1); k++) {

            var __element = document.createElement("div");

            if (quizNumber < 3 && quizmode == 0) {
                __element.setAttribute("class", "col");
                __element.setAttribute("style", "width:1018.77px;");
            } else {
                __element.setAttribute("class", "col-5");
            }

            var ___element = document.createElement("div");
            ___element.setAttribute("class", "row");

            if (quizmode) {
                ___element.setAttribute("style", "width:500px;text-align:center;");
            } else {
                ___element.setAttribute("style", "width:1000px;text-align:center;");
            }


            for (var j = 0; j < 2; j++) {
                //console.log("j loop:" + j);

                var temp = document.createElement("div");
                temp.setAttribute("class", "col");
                if (quizNumber >= 3 && quizmode == 1) {
                    temp.setAttribute("style", "padding: 0px;font-size: 15pt;");
                } else {
                    temp.setAttribute("style", "padding: 0px; text-align: right;");
                }

                if (quizNumber >= 3) {

                    temp.innerHTML = quizText[quizNumber - 3][(i + j * 10)]; //quizNumber % 2
                } else {
                    temp.innerHTML = String(1 + i + j * 15) + ".";
                }

                ___element.appendChild(temp);

                //console.log("phase 1");

                temp = document.createElement("div");
                temp.setAttribute("class", "col");
                temp.setAttribute("style", "padding: 0px;");

                var inputbox = document.createElement("input");
                inputbox.setAttribute("type", "text");
                inputbox.setAttribute("onchange", "typingTrigger()");
                inputbox.setAttribute("style", "height:25px; width:150px;border:1px; border-bottom-style: solid;border-top-style: none;border-left-style:none;border-right-style:none;");


                if (k) {
                    inputbox.setAttribute("readonly", "readonly");
                    inputbox.setAttribute("class", "mate msg");
                } else {
                    inputbox.setAttribute("class", "user msg");
                }

                inputbox.setAttribute("id", "msg" + (i + j * (quizNumber >= 3 ? 10 : 15)));

                //console.log("phase 2");

                temp.appendChild(inputbox);

                ___element.appendChild(temp); // row

            }


            __element.appendChild(___element); // col


            _element.appendChild(__element); // row

            var _nt = document.createElement("div");
            _nt.setAttribute("class", "col-1");
            _element.appendChild(_nt);



        }
        main_element.appendChild(_element);
    }
}