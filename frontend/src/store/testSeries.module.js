import { testSeriesService } from "@/api/testSeries.service";

export const testSeries = {
  namespaced: true,
  state: {
    all: {}
  },
  actions: {
    getAll({ commit }) {
      commit("getAllRequest");

      testSeriesService
        .getAll()
        .then(
          testSeries => commit("getAllSuccess", testSeries),
          error => commit("getAllFailure", error)
        );
    }
  },
  mutations: {
    getAllRequest(state) {
      state.all = { loading: true };
    },
    getAllSuccess(state, testSeries) {
      state.all = { items: testSeries };
    },
    getAllFailure(state, error) {
      state.all = { error };
    }
  }
};
