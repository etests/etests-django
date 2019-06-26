import { userService } from "@/api/user.service";

const user = JSON.parse(localStorage.getItem("user"));
const initialState = user
  ? { status: { loggedIn: true }, user }
  : { status: {}, user: null };

export const authentication = {
  namespaced: true,
  state: initialState,
  actions: {
    login({ dispatch, commit }, { username, password }) {
      commit("loginRequest", { name: username });

      userService.login(username, password).then(
        data => {
          commit("loginSuccess", data);
          setTimeout(() => {
            dispatch("alert/success", "Logged in successfully!", {
              root: true
            });
          });
        },
        error => {
          commit("loginFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    register({ dispatch, commit }, data) {
      commit("registerRequest", data);
      const credentials = {
        username: data.email || data.phone,
        password: data.password
      };

      userService.register(data).then(
        data => {
          commit("registerSuccess", data);
          setTimeout(() => {
            dispatch("login", credentials);
          });
        },
        error => {
          commit("registerFailure", error);
          dispatch("alert/error", error, { root: true });
        }
      );
    },
    logout({ dispatch, commit }) {
      userService.logout();
      commit("logout");
      setTimeout(() => {
        dispatch("alert/success", "See you soon!", {
          root: true
        });
      });
    }
  },
  mutations: {
    loginRequest(state, user) {
      state.status = { loggingIn: true };
      state.user = user;
    },
    loginSuccess(state, data) {
      state.status = { loggedIn: true };
      state.user = data.user;
    },
    loginFailure(state) {
      state.status = {};
      state.user = null;
    },
    logout(state) {
      state.status = {};
      state.user = null;
    },
    registerRequest(state, user) {
      state.status = { registering: true };
    },
    registerSuccess(state, user) {
      state.status = {};
    },
    registerFailure(state, error) {
      state.status = {};
    }
  }
};
