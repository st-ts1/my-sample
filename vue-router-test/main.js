// CDNのElementで日本語を使う
ELEMENT.locale(ELEMENT.lang.ja)

const mycomponent = {
        template: `<div>
        <h1>{{ welcome }}</h1>
        {{ mess }} {{ name }}
        </div>`,
    data: function () {
        return {
            mess: "ルータ内コンポーネントから参照した文字列→"
        }
    },
    props: ['name'],
    computed: {
        welcome: function() {
            let vm = this;
            console.log(vm.name);
            if (typeof vm.name == "undefined") {
                console.log("未定義");
                return "新規登録してください";
              }
            return "ようこそ " + vm.name;
        }
    }
};

var router = new VueRouter({
    routes: [
        {
            path: '/user/:name',
            component: mycomponent,
            // プロパティでコンポーネントに渡す
            props: true
        },
        {
            // マッチングの優先度は記載順。最後にマッチしなかったパターンを書く
            path: '*',
            component: mycomponent,
            props: true
        }
     ]
    });

new Vue({
    el: '#app',
    router: router,
    data: {
        "test": "Vueのテストです"
    }
}).$mount('#app');