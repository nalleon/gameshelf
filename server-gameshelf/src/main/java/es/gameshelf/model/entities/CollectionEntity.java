package es.gameshelf.model.entities;

import java.util.Objects;
import java.util.Set;

import jakarta.persistence.*;

/**
 * @author Nabil L. A. @nalleon
 */
@Entity
@Table(name ="collections")
@NamedQuery(name="CollectionEntity.findAll", query="SELECT r FROM CollectionEntity r")
public class CollectionEntity {

    /**
     * Properties
     */
    @Id
    @GeneratedValue(strategy= GenerationType.IDENTITY)
    @Column(unique=true, nullable=false)
    private int id;

    @OneToMany(mappedBy = "collection")
    private Set<GameCollectionItemEntity> gameCollectionSet;

    @ManyToOne()
    @JoinColumn(nullable=false, name = "user_id")
    private UserEntity userEntity;

    /**
     * Default constructor of the class
     */
    public CollectionEntity() {}

    /**
     * Constructor of the class
     * @param id of the collection
     */
    public CollectionEntity(int id) {
        this.id = id;
    }

    /**
     * Constructor of the class
     * @param userEntity of the collection
     * @implNote for creating a collection
     */
    public CollectionEntity(UserEntity userEntity) {
        this.userEntity = userEntity;
    }

    /**
     * Full constructor of the class
     * @param id of the collection
     * @param userEntity of the collection
     */
    public CollectionEntity(int id, UserEntity userEntity) {
        this.id = id;
        this.userEntity = userEntity;
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

    public UserEntity getUser() {
        return userEntity;
    }

    public void setUser(UserEntity userEntity) {
        this.userEntity = userEntity;
    }


    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        CollectionEntity collectionEntity = (CollectionEntity) o;
        return id == collectionEntity.id;
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(id);
    }

    @Override
    public String toString() {
        return "CollectionEntity{" +
                "id=" + id +
                ", userEntity=" + userEntity +
                '}';
    }
}

