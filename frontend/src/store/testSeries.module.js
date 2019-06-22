import { testSeriesService } from "@/api/testSeries.service";

const initialState = {
  status: {},
  testSeries: {},
  all: {}
};

export const testSeries = {
  namespaced: true,
  state: initialState,
  actions: {
    get({ dispatch, commit }, id) {
      commit("getRequest", id);

      testSeriesService.get(id).then(
        testSeries => {
          commit("getSuccess", testSeries);
          setTimeout(() => {
            dispatch("alert/success", "Test series fetched successfully!", {
              root: true
            });
          });
        },
        error => {
          commit("getFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    create({ dispatch, commit }, data) {
      commit("createRequest", data);

      testSeriesService.create(data).then(
        data => {
          commit("createSuccess", data);
          setTimeout(() => {
            dispatch("alert/success", "Test series created successfully!", {
              root: true
            });
          });
        },
        error => {
          commit("createFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    remove({ dispatch, commit }, id) {
      commit("removeRequest", id);

      testSeriesService.remove(id).then(
        _ => {
          commit("removeSuccess", id);
          setTimeout(() => {
            dispatch("alert/success", "Test series removed successfully!", {
              root: true
            });
          });
        },
        error => {
          commit("removeFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    getAll({ commit }) {
      commit("getAllRequest");

      testSeriesService
        .getAll()
        .then(
          testSeries => commit("getAllSuccess", testSeries),
          error => commit("getAllFailure", error)
        );
    },
    addTest({ commit }, test) {
      commit("addTestSuccess", test);
    }
  },
  mutations: {
    getRequest(state) {
      state.status = { loading: true };
    },
    getSuccess(state, testSeries) {
      state.status = {};
      state.testSeries = testSeries;
    },
    getFailure(state, error) {
      state.status = { error };
    },
    getAllRequest(state) {
      state.all = { loading: true };
    },
    getAllSuccess(state, testSeries) {
      state.all = { items: testSeries };
    },
    getAllFailure(state, error) {
      state.all = { error };
    },
    createRequest(state, data) {
      state.status = { creating: true };
    },
    createSuccess(state, data) {
      state.all.items.push(data);
      state.status = { created: true, testSeries: data };
    },
    createFailure(state, error) {
      state.status = { error: error };
    },
    removeRequest(state, id) {
      state.status = { removing: true, id: id };
    },
    removeSuccess(state, id) {
      state.status = { removed: true, id: id };
    },
    removeFailure(state, error) {
      state.status = { error: error };
    },
    addTestSuccess(state, test) {
      var targetTestSeries = state.all.items.filter(
        item => item.id === test.test_series
      );
      if (targetTestSeries.length) {
        targetTestSeries[0].tests.push(test);
      }
    }
  }
};
