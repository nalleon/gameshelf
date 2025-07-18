package es.gameshelf.model.entities;
import java.util.Objects;

/**
 * @author Nabil L. A. @nalleon
 */
public class RoleEntity {
    /**
     * Properties
     */
    private int id;
    private String name;

    /**
     * Default constructor of the class
     */
    public RoleEntity() {}

    /**
     * Constructor of the class
     * @param id of the role
     */
    public RoleEntity(int id) {
        this.id = id;
    }

    /**
     * Constructor of the class
     * @param name of the role
     */
    public RoleEntity(String name) {
        this.name = name;
    }

    /**
     * Full constructor of the class
     * @param id of the role
     * @param name of the role
     */
    public RoleEntity(int id, String name) {
        this.id = id;
        this.name = name;
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

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    /**
     * Equals and hashcode
     */
    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        RoleEntity that = (RoleEntity) o;
        return Objects.equals(name, that.name);
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(name);
    }

    @Override
    public String toString() {
        return "RoleEntity{" +
                "id=" + id +
                ", name='" + name + '\'' +
                '}';
    }
}
