import React, { useContext, useEffect, useState } from "react";
import "./Login.css";
import banner from "../../assets/banner.svg";
import AuthContext from "../../contexts/AuthContext";
import { checkAuth } from "../../utils/checkAuth";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
const Login = () => {
  const [showPassword, setShowPassword] = useState(false);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm();
  const navigate = useNavigate();

  const { login } = useContext(AuthContext);
  const toggleShowPassword = () => {
    setShowPassword(!showPassword);
  };

  const onSubmit = async (data) => {
    console.log(data);
    await login(data);
  };

  useEffect(() => {
    if (checkAuth()) {
      // navigate("/");
    }
  });

  return (
    <div className="login-container">
      <div className="login-form-wrapper">
        <div className="banner-container">
          <img src={banner} alt="eCitizen Banner" className="banner" />
        </div>
        <h2>Login</h2>
        <form noValidate onSubmit={handleSubmit(onSubmit)}>
          <div className="form-group">
            <label htmlFor="email" style={{ fontWeight: 100 }}>
              Email Adress
            </label>
            <input
              {...register("email", {
                validate: (value) => {
                  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/i.test(value)) {
                    return "Please enter a valid email address";
                  }
                },
                required: "Email is required",
              })}
              type="email"
              name="email"
              id="email"
            />
            {errors.email && (
              <span className="text-danger">{errors.email.message}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="password" style={{ fontWeight: 100 }}>
              Password
            </label>
            <div className="password-input-container">
              <input
                {...register("password", {
                  required: "Password is required",
                })}
                type={showPassword ? "text" : "password"}
                name="password"
                id="password"
              />
              <button
                type="button"
                onClick={toggleShowPassword}
                className="show-password-btn"
              >
                {showPassword ? "Hide" : "Show"}
              </button>
            </div>
            {errors.password && (
              <span className="text-danger">{errors.password.message}</span>
            )}
          </div>
          <button disabled={isSubmitting} type="submit">
            {isSubmitting ? "Signing you in..." : "Login"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
