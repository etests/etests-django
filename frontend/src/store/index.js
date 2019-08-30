import Vue from "vue";
import Vuex from "vuex";

import { alert } from "./alert.module";
import { authentication } from "./authentication.module";
import { users } from "./users.module";
import { institutes } from "./institutes.module";
import { testSeries } from "./testSeries.module";
import { tests } from "./tests.module";
import { sessions } from "./sessions.module";
import { results } from "./results.module";
import { reviews } from "./reviews.module";
import { batches } from "./batches.module";
import { transactions } from "./transactions.module";
import { credits } from "./credits.module";
import { enrollments } from "./enrollments.module";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    alert,
    authentication,
    users,
    institutes,
    testSeries,
    tests,
    sessions,
    results,
    reviews,
    batches,
    transactions,
    credits,
    enrollments
  }
});
