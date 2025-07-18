package es.gameshelf.model.entities.abstracts;

import jakarta.persistence.*;

import java.util.Objects;

/**
 * @author Nabil L. A. @nalleon
 */
@MappedSuperclass
public abstract class DetailsEntity {
    /**
     * Properties
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    @Column(nullable = false, unique = true)
    private String name;

    @Column(nullable = false, unique = true)
    private String additionalText;

    /**
     * Default constructor of the class
     */
    public DetailsEntity() {}

    /**
     * Constructor of the class
     * @param id of the detail
     */
    public DetailsEntity(int id) {
        this.id = id;
    }

    /**
     * Constructor of the class
     * @param name of the detail
     */
    public DetailsEntity(String name) {
        this.name = name;
    }

    /**
     * Constructor of the class
     * @param name of the detail
     * @param additionalText of the detail
     */
    public DetailsEntity(String name, String additionalText) {
        this.name = name;
        this.additionalText = additionalText;
    }

    /**
     * Full constructor of the class
     * @param id of the detail
     * @param name of the detail
     * @param additionalText of the detail
     */
    public DetailsEntity(int id, String name, String additionalText) {
        this.id = id;
        this.name = name;
        this.additionalText = additionalText;
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

    public String getAdditionalText() {
        return additionalText;
    }

    public void setAdditionalText(String additionalText) {
        this.additionalText = additionalText;
    }

    /**
     * Equals and hashcode
     */
    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        DetailsEntity that = (DetailsEntity) o;
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
                ", additionalText='" + additionalText + '\'' +
                '}';
    }
}
