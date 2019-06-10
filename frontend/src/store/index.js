import Vue from "vue";
import Vuex from "vuex";

import { alert } from "./alert.module";
import { authentication } from "./authentication.module";
import { users } from "./users.module";
import { institutes } from "./institutes.module";
import { testSeries } from "./testSeries.module";
import { tests } from "./tests.module";
import { unitTests } from "./unitTests.module";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    alert,
    authentication,
    users,
    institutes,
    testSeries,
    tests,
    unitTests
  }
});
