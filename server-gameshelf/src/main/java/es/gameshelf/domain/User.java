package es.gameshelf.domain;

import java.util.Date;
import java.util.Objects;

/**
 * @author Nabil L. A. @nalleon
 */
public class User {

    /**
     * Properties
     */
    private int id;
    private String username;
    private String email;
    private String password;
    private String profilePicture;
    private Role role;
    private int verified;
    private String verificationToken;
    private Date creationDate;

    /**
     * Default constructor of the class
     */
    public User() {
    }

    /**
     * Constructor of the class
     * @param id of the user
     */
    public User(int id) {
        this.id = id;
    }

    /**
     * Constructor of the class
     * @param username of the user
     */
    public User(String username) {
        this.username = username;
    }

    /**
     * Constructor of the class
     * @param username of the user
     * @param email of the user
     * @param password of the user
     * @implNote for creating a user
     */
    public User(String username, String email, String password) {
        this.username = username;
        this.email = email;
        this.password = password;
    }

    public User(int id, String username, String email, String password,
                String profilePicture, Role role) {
        this.id = id;
        this.username = username;
        this.email = email;
        this.password = password;
        this.profilePicture = profilePicture;
        this.role = role;
    }

    /**
     * Getters and setters
     */
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getProfilePicture() {
        return profilePicture;
    }

    public void setProfilePicture(String profilePicture) {
        this.profilePicture = profilePicture;
    }

    public int getVerified() {
        return verified;
    }

    public void setVerified(int verified) {
        this.verified = verified;
    }

    public String getVerificationToken() {
        return verificationToken;
    }

    public void setVerificationToken(String verificationToken) {
        this.verificationToken = verificationToken;
    }

    public Date getCreationDate() {
        return creationDate;
    }

    public void setCreationDate(Date creationDate) {
        this.creationDate = creationDate;
    }

    public Role getRole() {
        return role;
    }

    public void setRole(Role role) {
        this.role = role;
    }

    /**
     * Equals and hashcode
     */
    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        User user = (User) o;
        return id == user.id;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", username='" + username + '\'' +
                ", email='" + email + '\'' +
                ", profilePicture='" + profilePicture + '\'' +
                ", role=" + role +
                ", verified=" + verified +
                ", verificationToken='" + verificationToken + '\'' +
                ", creationDate=" + creationDate +
                '}';
    }
}
