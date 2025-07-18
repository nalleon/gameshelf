package es.gameshelf.model.entities;

import java.util.Date;
import java.util.Objects;

/**
 * @author Nabil L. A. @nalleon
 */
public class UserEntity {

    /**
     * Properties
     */
    private int id;
    private String username;
    private String email;
    private String password;
    private String profilePicture;
    private RoleEntity roleEntity;
    private int verified;
    private String verificationToken;
    private Date creationDate;

    /**
     * Default constructor of the class
     */
    public UserEntity() {
    }

    /**
     * Constructor of the class
     * @param id of the user
     */
    public UserEntity(int id) {
        this.id = id;
    }

    /**
     * Constructor of the class
     * @param username of the user
     */
    public UserEntity(String username) {
        this.username = username;
    }

    /**
     * Constructor of the class
     * @param username of the user
     * @param email of the user
     * @param password of the user
     * @implNote for creating a user
     */
    public UserEntity(String username, String email, String password) {
        this.username = username;
        this.email = email;
        this.password = password;
    }

    public UserEntity(int id, String username, String email, String password,
                      String profilePicture, RoleEntity roleEntity) {
        this.id = id;
        this.username = username;
        this.email = email;
        this.password = password;
        this.profilePicture = profilePicture;
        this.roleEntity = roleEntity;
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

    public RoleEntity getRole() {
        return roleEntity;
    }

    public void setRole(RoleEntity roleEntity) {
        this.roleEntity = roleEntity;
    }

    /**
     * Equals and hashcode
     */
    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        UserEntity userEntity = (UserEntity) o;
        return id == userEntity.id;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }

    @Override
    public String toString() {
        return "UserEntity{" +
                "id=" + id +
                ", username='" + username + '\'' +
                ", email='" + email + '\'' +
                ", profilePicture='" + profilePicture + '\'' +
                ", roleEntity=" + roleEntity +
                ", verified=" + verified +
                ", verificationToken='" + verificationToken + '\'' +
                ", creationDate=" + creationDate +
                '}';
    }
}
