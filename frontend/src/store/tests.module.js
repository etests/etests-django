import { testService } from "@/api/test.service";

const initialState = {
  status: {},
  test: {},
  all: { items: [] },
  rankLists: JSON.parse(localStorage.getItem("rankLists")) || []
};

export const tests = {
  namespaced: true,
  state: initialState,
  actions: {
    get({ dispatch, commit }, id) {
      commit("getRequest", id);

      testService.get(id).then(
        test => {
          commit("getSuccess", test);
        },
        error => {
          commit("getFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    create({ dispatch, commit }, data) {
      commit("createRequest", data);

      testService.create(data).then(
        data => {
          commit("createSuccess", data);
          setTimeout(() => {
            dispatch("alert/success", "Test created successfully!", {
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
    update({ dispatch, commit }, data) {
      commit("updateRequest", data);

      testService.update(data).then(
        data => {
          commit("updateSuccess", data);
          setTimeout(() => {
            dispatch("alert/success", "Test updated successfully!", {
              root: true
            });
            dispatch("testSeries/addTest", data, {
              root: true
            });
          });
        },
        error => {
          commit("updateFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    remove({ dispatch, commit }, id) {
      commit("removeRequest", id);

      testService.remove(id).then(
        _ => {
          commit("removeSuccess", id);
          setTimeout(() => {
            dispatch("alert/success", "Test deleted successfully!", {
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

      testService
        .getAll()
        .then(
          tests => commit("getAllSuccess", tests),
          error => commit("getAllFailure", error)
        );
    },
    generateRanks({ dispatch, commit }, id) {
      commit("generateRanksRequest");

      testService.generateRanks(id).then(
        message => {
          commit("generateRanksSuccess", message);
          dispatch("alert/success", message, {
            root: true
          });
        },
        error => {
          commit("generateRanksFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    getRankList({ dispatch, commit }, id) {
      commit("getRankListRequest", id);

      testService.getRankList(id).then(
        ranks => {
          commit("getRankListSuccess", { id, ranks });
          dispatch("alert/success", "Ranklist fetched successfully!", {
            root: true
          });
        },
        error => {
          commit("getRankListFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    }
  },
  mutations: {
    getRequest(state) {
      state.status = { loading: true };
    },
    getSuccess(state, test) {
      state.status = {};
      state.test = test;
    },
    getFailure(state, error) {
      state.status = { error };
    },
    getAllRequest(state) {
      state.status = { loading: true };
    },
    getAllSuccess(state, tests) {
      state.status = {exists: true};
      state.all = { items: tests };
    },
    getAllFailure(state, error) {
      state.status = { error };
    },
    generateRanksRequest(state) {
      state.status = { loading: true };
    },
    generateRanksSuccess(state, message) {
      state.status = { loaded: true, message };
    },
    generateRanksFailure(state, error) {
      state.status = { error };
    },
    createRequest(state, data) {
      state.status = { creating: true };
    },
    createSuccess(state, data) {
      if (data.test_series)
        this.dispatch("testSeries/addTest", data, {
          root: true
        });
      else state.all.items.push(data);
      state.status = { created: true, test: data };
    },
    createFailure(state, error) {
      state.status = { error: error };
    },
    updateRequest(state, data) {
      state.status = { updating: true };
    },
    updateSuccess(state, data) {
      state.status = { updated: true, test: data };
    },
    updateFailure(state, error) {
      state.status = { error: error };
    },
    removeRequest(state, id) {
      state.status = { removing: true, id: id };
    },
    removeSuccess(state, id) {
      state.status = { removed: true, id: id };
      state.all.items = state.all.items.filter(test => test.id !== id);
      this.dispatch("testSeries/removeTest", id, {
        root: true
      });
    },
    removeFailure(state, error) {
      state.status = { error: error };
    },
    getRankListRequest(state) {
      state.status = { loading: true };
    },
    getRankListSuccess(state, data) {
      state.status = { loaded: true };
      if (
        state.rankLists.findIndex(rankList => rankList.id === data.id) === -1
      ) {
        state.rankLists.push(data);
        localStorage.rankLists = JSON.stringify(state.rankLists);
      }
    },
    getRankListFailure(state, error) {
      state.status = { error };
    }
  }
};
