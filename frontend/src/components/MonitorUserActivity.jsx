import React, { useContext, useEffect, useState } from "react";
import { useIdleTimer } from "react-idle-timer";
import { isTokenAboutToExpire } from "../utils/checkAuth";
import AuthContext from "../contexts/AuthContext";
import { Config } from "../Config";

const timeout = Config.IDLE_TIMEOUT;
const promptBeforeIdle = Config.PROMPT_BEFORE_IDLE; //prompt user before idle timeout

const MonitorUserActivity = () => {
  const [state, setState] = useState("Active");
  const [remaining, setRemaining] = useState(timeout);
  const [open, setOpen] = useState(false);
  const { getNewAccessToken, logout } = useContext(AuthContext);
  const [doLogin, setDoLogin] = useState(false);

  const onIdle = () => {
    setState("Idle");
    setOpen(true);
    //user is very idle log him out
    logout();
  };

  const onActive = () => {
    setState("Active");
    setOpen(false);
  };

  const onPrompt = () => {
    setState("Prompted");
    setOpen(true);
  };

  const { getRemainingTime, activate } = useIdleTimer({
    onIdle,
    onActive,
    onPrompt,
    timeout,
    promptBeforeIdle,
    throttle: 500,
  });

  useEffect(() => {
    console.log(state);

    if (isTokenAboutToExpire()) {
      console.log("Token about to expire");
      if (!doLogin) {
        setDoLogin(true);
        getNewAccessToken();
      }
    }

    const interval = setInterval(() => {
      setRemaining(Math.ceil(getRemainingTime() / 1000));
    }, 500);

    return () => {
      clearInterval(interval);
    };
  });

  const handleStillHere = () => {
    activate();
  };

  const timeTillPrompt = Math.max(remaining - promptBeforeIdle / 1000, 0);
  const seconds = timeTillPrompt > 1 ? "seconds" : "second";

  return (
    <div>
      <div
        className="modal"
        style={{
          display: open ? "flex" : "none",
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: "crimson",
          height: "55px",
        }}
      >
        <h3>Are you still here?</h3>
        <p>Logging out in {remaining} seconds</p>&nbsp;&nbsp;
        <button onClick={handleStillHere}>Im Still Here</button>
      </div>
    </div>
  );
};

export default MonitorUserActivity;
