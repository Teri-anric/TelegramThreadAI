import { Link } from "react-router-dom";
import Profile from "../profile/Profile";
import "./header.css";

const Header = () => {
    return (
        <nav className="header-nav">
            <Link to="/">Home</Link>
            <Profile />
        </nav>
    );
};

export default Header;