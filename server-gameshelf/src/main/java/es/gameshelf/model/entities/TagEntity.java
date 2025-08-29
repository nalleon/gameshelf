package es.gameshelf.model.entities;

import es.gameshelf.model.entities.abstracts.ClassificationEntity;
import jakarta.persistence.*;

import java.util.Set;

/**
 * @author Nabil L. A. @nalleon
 */
@Entity
@Table(name="tags")
@NamedQuery(name="TagEntity.findAll", query="SELECT r FROM TagEntity r")
public class TagEntity extends ClassificationEntity {


    @ManyToMany(mappedBy = "tagEntitySet", cascade = CascadeType.PERSIST,fetch = FetchType.LAZY)
    Set<GameEntity> games;

    /**
     * Default constructor of the class
     */
    public TagEntity() {
    }

    /**
     * Constructor of the class
     * @param id of the tag
     */
    public TagEntity(int id) {
        super(id);
    }

    /**
     * Constructor of the class
     * @param name of the tag
     */
    public TagEntity(String name) {
        super(name);
    }

    /**
     * Full constructor of the class
     * @param id of the tag
     * @param name of the tag
     */
    public TagEntity(int id, String name) {
        super(id, name);
    }
}
