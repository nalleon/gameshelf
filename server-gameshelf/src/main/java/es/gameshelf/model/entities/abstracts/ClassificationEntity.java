package es.gameshelf.model.entities.abstracts;

import jakarta.persistence.*;

import java.util.Objects;

/**
 * @author Nabil L. A. @nalleon
 */
@MappedSuperclass
public abstract class ClassificationEntity {
    /**
     * Properties
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    @Column(nullable = false, unique = true)
    private String name;

    /**
     * Default constructor of the class
     */
    public ClassificationEntity() {}

    /**
     * Constructor of the class
     * @param id of the classification
     */
    public ClassificationEntity(int id) {
        this.id = id;
    }

    /**
     * Constructor of the class
     * @param name of the classification
     */
    public ClassificationEntity(String name) {
        this.name = name;
    }

    /**
     * Full constructor of the class
     * @param id of the classification
     * @param name of the classification
     */
    public ClassificationEntity(int id, String name) {
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
        ClassificationEntity that = (ClassificationEntity) o;
        return Objects.equals(name, that.name);
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(name);
    }

    @Override
    public String toString() {
        return getClass().getSimpleName()+"{" +
                "id=" + id +
                ", name='" + name + '\'' +
                '}';
    }
}
